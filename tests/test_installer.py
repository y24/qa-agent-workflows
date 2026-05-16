from pathlib import Path
import shutil
import uuid

import pytest

from qa_workflow_toolkit.installer import (
    apply_default_actions,
    build_install_plan,
    install_from_plan,
    next_available_agents_path,
)
from qa_workflow_toolkit.models import CollisionAction
from qa_workflow_toolkit.registry import get_workflow


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


def test_next_available_agents_path(workspace_tmp: Path) -> None:
    (workspace_tmp / "AGENTS.md").write_text("existing", encoding="utf-8")
    (workspace_tmp / "AGENTS_1.md").write_text("existing", encoding="utf-8")

    assert next_available_agents_path(workspace_tmp / "AGENTS.md") == workspace_tmp / "AGENTS_2.md"
