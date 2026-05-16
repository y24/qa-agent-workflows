from pathlib import Path
import shutil
import uuid

import pytest

from qa_workflow_toolkit.state import load_installed_workflows, remove_installed_workflows, save_installed_workflows


@pytest.fixture()
def workspace_tmp() -> Path:
    path = Path("work") / "test-tmp" / f"qatool-state-test-{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def test_save_installed_workflows_removes_empty_state_file(workspace_tmp) -> None:
    state_dir = workspace_tmp / ".qa-toolkit"
    state_dir.mkdir()
    (state_dir / "workflows.json").write_text('{"schema_version": 1, "workflows": []}\n', encoding="utf-8")
    (state_dir / "other.json").write_text("{}", encoding="utf-8")

    save_installed_workflows(workspace_tmp, {})

    assert state_dir.exists()
    assert not (state_dir / "workflows.json").exists()
    assert (state_dir / "other.json").is_file()
    assert load_installed_workflows(workspace_tmp) == {}


def test_remove_installed_workflows_removes_empty_state_file(workspace_tmp) -> None:
    state_dir = workspace_tmp / ".qa-toolkit"
    state_dir.mkdir()
    (state_dir / "workflows.json").write_text(
        """{
  "schema_version": 1,
  "workflows": [
    {
      "workflow_id": "scenario-test-design",
      "agent": "roocode",
      "include_agents_md": true,
      "manifest_version": "1.0.0",
      "installed_at": "2026-05-16T00:00:00+00:00",
      "updated_at": "2026-05-16T00:00:00+00:00"
    }
  ]
}
""",
        encoding="utf-8",
    )

    remove_installed_workflows(workspace_tmp, ["scenario-test-design"])

    assert state_dir.exists()
    assert not (state_dir / "workflows.json").exists()
