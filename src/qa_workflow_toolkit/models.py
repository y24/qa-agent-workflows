from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from .agents import supported_agent_ids


class CollisionAction(str, Enum):
    OVERWRITE = "overwrite"
    SKIP = "skip"
    RENAME = "rename"
    NO_CHANGE = "no change"


@dataclass(frozen=True)
class InstallSourceTarget:
    source: str
    target: str


@dataclass(frozen=True)
class WorkflowInstallSpec:
    shared: InstallSourceTarget
    skill: InstallSourceTarget
    command: InstallSourceTarget


@dataclass(frozen=True)
class WorkflowManifest:
    id: str
    display_name: str
    description: str
    version: str
    sort_order: int | None
    skill_name: str
    command_name: str
    supported_agents: tuple[str, ...]
    default_agent: str
    install: WorkflowInstallSpec
    post_install_message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WorkflowManifest":
        required = [
            "id",
            "display_name",
            "description",
            "version",
            "skill_name",
            "command_name",
            "default_agent",
            "install",
            "post_install_message",
        ]
        missing = [key for key in required if key not in data]
        if missing:
            raise ValueError(f"workflow manifest is missing required fields: {', '.join(missing)}")

        install = data["install"]
        return cls(
            id=str(data["id"]),
            display_name=str(data["display_name"]),
            description=str(data["description"]),
            version=str(data["version"]),
            sort_order=int(data["sort_order"]) if data.get("sort_order") is not None else None,
            skill_name=str(data["skill_name"]),
            command_name=str(data["command_name"]),
            supported_agents=tuple(str(agent) for agent in data.get("supported_agents") or supported_agent_ids()),
            default_agent=str(data["default_agent"]),
            install=WorkflowInstallSpec(
                shared=InstallSourceTarget(**install["shared"]),
                skill=InstallSourceTarget(**install["skill"]),
                command=InstallSourceTarget(**install["command"]),
            ),
            post_install_message=str(data["post_install_message"]),
        )


@dataclass(frozen=True)
class WikiTypeManifest:
    id: str
    display_name: str
    description: str
    version: str
    sort_order: int | None
    is_default: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WikiTypeManifest":
        required = [
            "id",
            "display_name",
            "description",
            "version",
        ]
        missing = [key for key in required if key not in data]
        if missing:
            raise ValueError(f"wiki type manifest is missing required fields: {', '.join(missing)}")

        return cls(
            id=str(data["id"]),
            display_name=str(data["display_name"]),
            description=str(data["description"]),
            version=str(data["version"]),
            sort_order=int(data["sort_order"]) if data.get("sort_order") is not None else None,
            is_default=bool(data.get("default", False)),
        )


@dataclass(frozen=True)
class InstallPlanItem:
    kind: str
    source: str
    target: Path
    exists: bool
    is_dir: bool
    action: CollisionAction | None = None


@dataclass(frozen=True)
class InstallResult:
    copied: tuple[Path, ...]
    skipped: tuple[Path, ...]
    renamed: tuple[Path, ...]


@dataclass(frozen=True)
class UninstallPlanItem:
    kind: str
    source: str
    target: Path
    exists: bool
    is_dir: bool
    safe_to_remove: bool


@dataclass(frozen=True)
class UninstallResult:
    removed: tuple[Path, ...]
    skipped: tuple[Path, ...]
