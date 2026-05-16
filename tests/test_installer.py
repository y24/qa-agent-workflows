from pathlib import Path
import shutil
import uuid

import pytest

from qa_workflow_toolkit.installer import (
    apply_default_actions,
    asset_exactly_matches_path,
    build_install_plan,
    build_uninstall_plan,
    install_from_plan,
    next_available_agents_path,
    uninstall_from_plan,
)
from qa_workflow_toolkit.models import CollisionAction
from qa_workflow_toolkit.registry import get_workflow
from qa_workflow_toolkit.wiki import build_wiki_init_items


@pytest.fixture()
def workspace_tmp() -> Path:
    path = Path("work") / "test-tmp" / f"qatool-test-{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def test_build_install_plan_for_scenario_test_design(workspace_tmp: Path) -> None:
    workflow = get_workflow("scenario-test-design")
    plan = build_install_plan(workflow, workspace_tmp, "roocode")

    assert [item.kind for item in plan] == ["agents_md", "shared", "skill", "command"]
    assert plan[0].target == workspace_tmp / "AGENTS.md"
    assert plan[2].target == workspace_tmp / ".agents" / "skills" / "scenario-test-design"
    assert plan[3].target == workspace_tmp / ".roo" / "commands" / "scenario-test-design.md"


def test_build_install_plan_uses_agent_specific_command_target(workspace_tmp: Path) -> None:
    workflow = get_workflow("scenario-test-design")
    plan = build_install_plan(workflow, workspace_tmp, "claude")

    assert plan[3].source == "commands/scenario-test-design.md"
    assert plan[3].target == workspace_tmp / ".claude" / "commands" / "scenario-test-design.md"


def test_build_wiki_init_items_uses_agent_specific_command_target(workspace_tmp: Path) -> None:
    items = build_wiki_init_items(workspace_tmp, "research-notes", "claude")
    command_targets = {item.target for item in items if item.kind == "command"}

    assert workspace_tmp / ".claude" / "commands" / "ingest.md" in command_targets
    assert workspace_tmp / ".roo" / "commands" / "ingest.md" not in command_targets
    assert "skill" not in {item.kind for item in items}


def test_build_install_plan_can_skip_agents_md(workspace_tmp: Path) -> None:
    workflow = get_workflow("scenario-test-design")
    plan = build_install_plan(workflow, workspace_tmp, "roocode", include_agents_md=False)

    assert [item.kind for item in plan] == ["shared", "skill", "command"]
    assert all(item.target != workspace_tmp / "AGENTS.md" for item in plan)


def test_install_copies_assets(workspace_tmp: Path) -> None:
    workflow = get_workflow("scenario-test-design")
    plan = build_install_plan(workflow, workspace_tmp, "roocode")
    plan = apply_default_actions(plan, CollisionAction.OVERWRITE)

    result = install_from_plan(plan)

    assert len(result.copied) == 4
    assert (workspace_tmp / "AGENTS.md").is_file()
    assert (workspace_tmp / ".agents" / "shared" / "common_contract.md").is_file()
    assert (workspace_tmp / ".agents" / "skills" / "scenario-test-design" / "SKILL.md").is_file()
    assert (workspace_tmp / ".roo" / "commands" / "scenario-test-design.md").is_file()


def test_build_install_plan_marks_matching_existing_assets_as_no_change(workspace_tmp: Path) -> None:
    workflow = get_workflow("scenario-test-design")
    initial_plan = apply_default_actions(build_install_plan(workflow, workspace_tmp, "roocode"), CollisionAction.OVERWRITE)
    install_from_plan(initial_plan)

    plan = build_install_plan(workflow, workspace_tmp, "roocode")

    assert {item.action for item in plan} == {CollisionAction.NO_CHANGE}


def test_install_skips_no_change_items(workspace_tmp: Path) -> None:
    workflow = get_workflow("scenario-test-design")
    initial_plan = apply_default_actions(build_install_plan(workflow, workspace_tmp, "roocode"), CollisionAction.OVERWRITE)
    install_from_plan(initial_plan)
    plan = build_install_plan(workflow, workspace_tmp, "roocode")

    result = install_from_plan(plan)

    assert result.copied == ()
    assert len(result.skipped) == 4


def test_uninstall_removes_matching_workflow_assets(workspace_tmp: Path) -> None:
    workflow = get_workflow("scenario-test-design")
    initial_plan = apply_default_actions(build_install_plan(workflow, workspace_tmp, "roocode"), CollisionAction.OVERWRITE)
    install_from_plan(initial_plan)
    plan = build_uninstall_plan(workflow, workspace_tmp, "roocode")

    result = uninstall_from_plan(plan)

    assert len(result.removed) == 2
    assert not (workspace_tmp / ".agents" / "skills" / "scenario-test-design").exists()
    assert not (workspace_tmp / ".roo" / "commands" / "scenario-test-design.md").exists()
    assert (workspace_tmp / ".agents" / "shared" / "common_contract.md").is_file()
    assert (workspace_tmp / "AGENTS.md").is_file()


def test_uninstall_skips_modified_assets(workspace_tmp: Path) -> None:
    workflow = get_workflow("scenario-test-design")
    initial_plan = apply_default_actions(build_install_plan(workflow, workspace_tmp, "roocode"), CollisionAction.OVERWRITE)
    install_from_plan(initial_plan)
    command_path = workspace_tmp / ".roo" / "commands" / "scenario-test-design.md"
    command_path.write_text("modified", encoding="utf-8")
    plan = build_uninstall_plan(workflow, workspace_tmp, "roocode")

    result = uninstall_from_plan(plan)

    assert command_path in result.skipped
    assert command_path.is_file()


def test_uninstall_does_not_count_missing_assets_as_skipped(workspace_tmp: Path) -> None:
    workflow = get_workflow("scenario-test-design")
    initial_plan = apply_default_actions(
        build_install_plan(workflow, workspace_tmp, "roocode", include_agents_md=False),
        CollisionAction.OVERWRITE,
    )
    install_from_plan(initial_plan)
    plan = build_uninstall_plan(workflow, workspace_tmp, "roocode", include_agents_md=True)

    result = uninstall_from_plan(plan)

    assert workspace_tmp / "AGENTS.md" not in result.skipped
    assert result.skipped == ()


def test_asset_exactly_matches_path_rejects_extra_directory_files(workspace_tmp: Path) -> None:
    workflow = get_workflow("scenario-test-design")
    initial_plan = apply_default_actions(build_install_plan(workflow, workspace_tmp, "roocode"), CollisionAction.OVERWRITE)
    install_from_plan(initial_plan)
    (workspace_tmp / ".agents" / "skills" / "scenario-test-design" / "extra.md").write_text("extra", encoding="utf-8")

    assert not asset_exactly_matches_path(
        workflow.install.skill.source,
        workspace_tmp / ".agents" / "skills" / "scenario-test-design",
    )


def test_next_available_agents_path(workspace_tmp: Path) -> None:
    (workspace_tmp / "AGENTS.md").write_text("existing", encoding="utf-8")
    (workspace_tmp / "AGENTS_1.md").write_text("existing", encoding="utf-8")

    assert next_available_agents_path(workspace_tmp / "AGENTS.md") == workspace_tmp / "AGENTS_2.md"
