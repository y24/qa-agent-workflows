from pathlib import Path
import json
import shutil
import uuid

import pytest

from qa_workflow_toolkit.state import (
    AGENTS_MD_KIND_WIKI,
    InstalledWorkflow,
    load_installed_workflows,
    load_repository_config,
    record_repository_config,
    remove_installed_workflows,
    save_installed_workflows,
)


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
  "agent": "roocode",
  "include_agents_md": true,
  "workflows": [
    {
      "workflow_id": "scenario-test-design",
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


def test_save_installed_workflows_stores_agent_config_once(workspace_tmp) -> None:
    save_installed_workflows(
        workspace_tmp,
        {
            "scenario-test-design": InstalledWorkflow(
                workflow_id="scenario-test-design",
                agent="roocode",
                include_agents_md=False,
                manifest_version="1.0.0",
                installed_at="2026-05-16T00:00:00+00:00",
                updated_at="2026-05-16T00:00:00+00:00",
            )
        },
    )

    data = json.loads((workspace_tmp / ".qa-toolkit" / "workflows.json").read_text(encoding="utf-8"))

    assert data["agent"] == "roocode"
    assert data["include_agents_md"] is False
    assert "agent" not in data["workflows"][0]
    assert "include_agents_md" not in data["workflows"][0]


def test_load_installed_workflows_reads_top_level_agent_config(workspace_tmp) -> None:
    state_dir = workspace_tmp / ".qa-toolkit"
    state_dir.mkdir()
    (state_dir / "workflows.json").write_text(
        """{
  "schema_version": 1,
  "agent": "roocode",
  "include_agents_md": false,
  "workflows": [
    {
      "workflow_id": "scenario-test-design",
      "manifest_version": "1.0.0",
      "installed_at": "2026-05-16T00:00:00+00:00",
      "updated_at": "2026-05-16T00:00:00+00:00"
    }
  ]
}
""",
        encoding="utf-8",
    )

    installed = load_installed_workflows(workspace_tmp)

    assert installed["scenario-test-design"].agent == "roocode"
    assert installed["scenario-test-design"].include_agents_md is False


def test_record_repository_config_can_store_agent_without_workflows(workspace_tmp) -> None:
    record_repository_config(workspace_tmp, "roocode", include_agents_md=False, agents_md_kind=AGENTS_MD_KIND_WIKI)

    data = json.loads((workspace_tmp / ".qa-toolkit" / "workflows.json").read_text(encoding="utf-8"))
    config = load_repository_config(workspace_tmp)

    assert data["agent"] == "roocode"
    assert data["include_agents_md"] is False
    assert data["agents_md_kind"] == "wiki"
    assert data["workflows"] == []
    assert config is not None
    assert config.agent == "roocode"
    assert config.include_agents_md is False
    assert config.agents_md_kind == "wiki"
    assert load_installed_workflows(workspace_tmp) == {}
