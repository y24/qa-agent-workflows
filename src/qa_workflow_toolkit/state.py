from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import WorkflowManifest

STATE_DIR_NAME = ".qa-toolkit"
STATE_FILE_NAME = "workflows.json"
STATE_SCHEMA_VERSION = 1
DEFAULT_AGENT = "roocode"


@dataclass(frozen=True)
class InstalledWorkflow:
    workflow_id: str
    agent: str
    include_agents_md: bool
    manifest_version: str
    installed_at: str
    updated_at: str


@dataclass(frozen=True)
class RepositoryConfig:
    agent: str
    include_agents_md: bool


def state_file_path(target: Path) -> Path:
    return target / STATE_DIR_NAME / STATE_FILE_NAME


def load_repository_config(target: Path) -> RepositoryConfig | None:
    data = _load_state_data(target)
    if not data or "agent" not in data:
        return None
    return RepositoryConfig(
        agent=str(data["agent"]),
        include_agents_md=bool(data.get("include_agents_md", True)),
    )


def load_installed_workflows(target: Path) -> dict[str, InstalledWorkflow]:
    data = _load_state_data(target)
    if not data:
        return {}

    workflows = data.get("workflows", [])
    agent = str(data.get("agent", DEFAULT_AGENT))
    include_agents_md = bool(data.get("include_agents_md", True))
    installed: dict[str, InstalledWorkflow] = {}
    for item in workflows:
        workflow_id = str(item["workflow_id"])
        installed[workflow_id] = InstalledWorkflow(
            workflow_id=workflow_id,
            agent=agent,
            include_agents_md=include_agents_md,
            manifest_version=str(item.get("manifest_version", "")),
            installed_at=str(item.get("installed_at", "")),
            updated_at=str(item.get("updated_at", "")),
        )
    return installed


def save_installed_workflows(target: Path, workflows: dict[str, InstalledWorkflow]) -> None:
    config = load_repository_config(target)
    _save_installed_workflows(
        target,
        workflows,
        agent=config.agent if config else None,
        include_agents_md=config.include_agents_md if config else None,
        keep_empty=config is not None,
    )


def record_repository_config(target: Path, agent: str, include_agents_md: bool = True) -> None:
    _save_installed_workflows(
        target,
        load_installed_workflows(target),
        agent=agent,
        include_agents_md=include_agents_md,
        keep_empty=True,
    )


def _save_installed_workflows(
    target: Path,
    workflows: dict[str, InstalledWorkflow],
    agent: str | None = None,
    include_agents_md: bool | None = None,
    keep_empty: bool = False,
) -> None:
    path = state_file_path(target)
    if not workflows and not keep_empty:
        path.unlink(missing_ok=True)
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    agent = agent or _single_workflow_value(workflows, "agent", DEFAULT_AGENT)
    include_agents_md = (
        include_agents_md
        if include_agents_md is not None
        else _single_workflow_value(workflows, "include_agents_md", True)
    )
    data: dict[str, Any] = {
        "schema_version": STATE_SCHEMA_VERSION,
        "agent": agent,
        "include_agents_md": include_agents_md,
        "workflows": [
            {
                "workflow_id": workflow.workflow_id,
                "manifest_version": workflow.manifest_version,
                "installed_at": workflow.installed_at,
                "updated_at": workflow.updated_at,
            }
            for workflow in sorted(workflows.values(), key=lambda item: item.workflow_id)
        ],
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def record_installed_workflows(
    target: Path,
    workflows: list[WorkflowManifest],
    agent: str,
    include_agents_md: bool,
) -> None:
    installed = load_installed_workflows(target)
    now = _now_iso()
    for workflow in workflows:
        existing = installed.get(workflow.id)
        installed[workflow.id] = InstalledWorkflow(
            workflow_id=workflow.id,
            agent=agent,
            include_agents_md=include_agents_md,
            manifest_version=workflow.version,
            installed_at=existing.installed_at if existing else now,
            updated_at=now,
        )
    _save_installed_workflows(target, installed, agent=agent, include_agents_md=include_agents_md, keep_empty=True)


def remove_installed_workflows(target: Path, workflow_ids: list[str]) -> None:
    installed = load_installed_workflows(target)
    had_workflows = bool(installed)
    config = load_repository_config(target)
    for workflow_id in workflow_ids:
        installed.pop(workflow_id, None)
    _save_installed_workflows(
        target,
        installed,
        agent=config.agent if config else None,
        include_agents_md=config.include_agents_md if config else None,
        keep_empty=not had_workflows and config is not None,
    )


def _load_state_data(target: Path) -> dict[str, Any] | None:
    path = state_file_path(target)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _single_workflow_value(workflows: dict[str, InstalledWorkflow], field_name: str, default: Any) -> Any:
    values = {getattr(workflow, field_name) for workflow in workflows.values()}
    if len(values) == 1:
        return next(iter(values))
    return default
