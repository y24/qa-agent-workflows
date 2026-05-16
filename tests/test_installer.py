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


def test_build_install_plan_for_test_design(workspace_tmp: Path) -> None:
    workflow = get_workflow("test-design")
    plan = build_install_plan(workflow, workspace_tmp, "roocode")

    assert [item.kind for item in plan] == ["agents_md", "shared", "skill", "command"]
    assert plan[0].target == workspace_tmp / "AGENTS.md"
    assert plan[2].target == workspace_tmp / ".agents" / "skills" / "test-design"
    assert plan[3].target == workspace_tmp / ".roo" / "commands" / "test-design.md"


def test_install_copies_assets(workspace_tmp: Path) -> None:
    workflow = get_workflow("test-design")
    plan = build_install_plan(workflow, workspace_tmp, "roocode")
    plan = apply_default_actions(plan, CollisionAction.OVERWRITE)

    result = install_from_plan(plan)

    assert len(result.copied) == 4
    assert (workspace_tmp / "AGENTS.md").is_file()
    assert (workspace_tmp / ".agents" / "shared" / "common_contract.md").is_file()
    assert (workspace_tmp / ".agents" / "skills" / "test-design" / "SKILL.md").is_file()
    assert (workspace_tmp / ".roo" / "commands" / "test-design.md").is_file()


def test_next_available_agents_path(workspace_tmp: Path) -> None:
    (workspace_tmp / "AGENTS.md").write_text("existing", encoding="utf-8")
    (workspace_tmp / "AGENTS_1.md").write_text("existing", encoding="utf-8")

    assert next_available_agents_path(workspace_tmp / "AGENTS.md") == workspace_tmp / "AGENTS_2.md"
