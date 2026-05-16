from __future__ import annotations

import shutil
from pathlib import Path

from importlib.resources.abc import Traversable

from .agents import get_agent_spec
from .models import CollisionAction, InstallPlanItem, InstallResult, UninstallPlanItem, UninstallResult, WorkflowManifest
from .paths import workflow_asset_path


def build_install_plan(
    workflow: WorkflowManifest,
    target_dir: Path,
    agent: str,
    include_agents_md: bool = True,
) -> list[InstallPlanItem]:
    if agent not in workflow.supported_agents:
        raise ValueError(f"{workflow.id} does not support agent: {agent}")

    agent_spec = get_agent_spec(agent)
    items: list[InstallPlanItem] = []
    if include_agents_md and workflow.install.agents_md:
        items.append(_plan_item("agents_md", agent_spec.agents_md_source, target_dir / "AGENTS.md"))

    items.append(_plan_item("shared", workflow.install.shared.source, target_dir / workflow.install.shared.target))
    items.append(_plan_item("skill", workflow.install.skill.source, target_dir / workflow.install.skill.target))
    items.append(_plan_item("command", workflow.install.command.source, _command_target(workflow, target_dir, agent)))
    return items


def apply_default_actions(plan: list[InstallPlanItem], action: CollisionAction) -> list[InstallPlanItem]:
    return [
        InstallPlanItem(
            kind=item.kind,
            source=item.source,
            target=item.target,
            exists=item.exists,
            is_dir=item.is_dir,
            action=(
                item.action
                if item.action == CollisionAction.NO_CHANGE
                else action if item.exists else CollisionAction.OVERWRITE
            ),
        )
        for item in plan
    ]


def install_from_plan(plan: list[InstallPlanItem]) -> InstallResult:
    copied: list[Path] = []
    skipped: list[Path] = []
    renamed: list[Path] = []

    for item in plan:
        action = item.action or (CollisionAction.SKIP if item.exists else CollisionAction.OVERWRITE)
        if action == CollisionAction.NO_CHANGE:
            skipped.append(item.target)
            continue

        if item.exists and action == CollisionAction.SKIP:
            skipped.append(item.target)
            continue

        target = item.target
        if item.exists and action == CollisionAction.RENAME:
            target = next_available_agents_path(item.target)
            renamed.append(target)

        source = workflow_asset_path(item.source)
        _copy_resource(source, target, overwrite=action == CollisionAction.OVERWRITE)
        copied.append(target)

    return InstallResult(copied=tuple(copied), skipped=tuple(skipped), renamed=tuple(renamed))


def build_uninstall_plan(
    workflow: WorkflowManifest,
    target_dir: Path,
    agent: str,
    include_shared: bool = False,
    include_agents_md: bool = False,
) -> list[UninstallPlanItem]:
    if agent not in workflow.supported_agents:
        raise ValueError(f"{workflow.id} does not support agent: {agent}")

    agent_spec = get_agent_spec(agent)
    items: list[UninstallPlanItem] = []
    if include_agents_md and workflow.install.agents_md:
        items.append(_uninstall_plan_item("agents_md", agent_spec.agents_md_source, target_dir / "AGENTS.md"))
    if include_shared:
        items.append(_uninstall_plan_item("shared", workflow.install.shared.source, target_dir / workflow.install.shared.target))

    items.append(_uninstall_plan_item("skill", workflow.install.skill.source, target_dir / workflow.install.skill.target))
    items.append(_uninstall_plan_item("command", workflow.install.command.source, _command_target(workflow, target_dir, agent)))
    return items


def _command_target(workflow: WorkflowManifest, target_dir: Path, agent: str) -> Path:
    agent_spec = get_agent_spec(agent)
    return target_dir / agent_spec.command_target_dir / f"{workflow.command_name}.md"


def uninstall_from_plan(plan: list[UninstallPlanItem]) -> UninstallResult:
    removed: list[Path] = []
    skipped: list[Path] = []

    for item in plan:
        if not item.exists:
            continue

        if not item.safe_to_remove:
            skipped.append(item.target)
            continue

        if item.is_dir:
            shutil.rmtree(item.target)
        else:
            item.target.unlink()
        removed.append(item.target)

    return UninstallResult(removed=tuple(removed), skipped=tuple(skipped))


def next_available_agents_path(path: Path) -> Path:
    for index in range(1, 1000):
        candidate = path.with_name(f"{path.stem}_{index}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"could not find available filename for {path}")


def asset_matches_path(source: str, target: Path) -> bool:
    source_resource = workflow_asset_path(source)
    if not source_resource.exists():
        raise FileNotFoundError(f"asset not found: {source}")
    return target.exists() and _resource_matches_path(source_resource, target)


def asset_exactly_matches_path(source: str, target: Path) -> bool:
    source_resource = workflow_asset_path(source)
    if not source_resource.exists():
        raise FileNotFoundError(f"asset not found: {source}")
    return target.exists() and _resource_exactly_matches_path(source_resource, target)


def _plan_item(kind: str, source: str, target: Path) -> InstallPlanItem:
    source_resource = workflow_asset_path(source)
    if not source_resource.exists():
        raise FileNotFoundError(f"asset not found: {source}")
    action = CollisionAction.NO_CHANGE if asset_matches_path(source, target) else None
    return InstallPlanItem(
        kind=kind,
        source=source,
        target=target,
        exists=target.exists(),
        is_dir=source_resource.is_dir(),
        action=action,
    )


def _uninstall_plan_item(kind: str, source: str, target: Path) -> UninstallPlanItem:
    source_resource = workflow_asset_path(source)
    if not source_resource.exists():
        raise FileNotFoundError(f"asset not found: {source}")
    return UninstallPlanItem(
        kind=kind,
        source=source,
        target=target,
        exists=target.exists(),
        is_dir=source_resource.is_dir(),
        safe_to_remove=asset_exactly_matches_path(source, target),
    )


def _copy_resource(source: Traversable, target: Path, overwrite: bool) -> None:
    if source.is_dir():
        if target.exists() and overwrite:
            shutil.rmtree(target)
        target.mkdir(parents=True, exist_ok=True)
        for child in source.iterdir():
            _copy_resource(child, target / child.name, overwrite=overwrite)
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not overwrite:
        return
    with source.open("rb") as input_file, target.open("wb") as output_file:
        shutil.copyfileobj(input_file, output_file)


def _resource_matches_path(source: Traversable, target: Path) -> bool:
    if source.is_dir():
        if not target.is_dir():
            return False
        source_children = sorted(source.iterdir(), key=lambda child: child.name)
        return all(_resource_matches_path(source_child, target / source_child.name) for source_child in source_children)

    if not target.is_file():
        return False
    with source.open("rb") as source_file, target.open("rb") as target_file:
        return source_file.read() == target_file.read()


def _resource_exactly_matches_path(source: Traversable, target: Path) -> bool:
    if source.is_dir():
        if not target.is_dir():
            return False
        source_children = sorted(source.iterdir(), key=lambda child: child.name)
        target_children = sorted(target.iterdir(), key=lambda child: child.name)
        if [child.name for child in source_children] != [child.name for child in target_children]:
            return False
        return all(_resource_exactly_matches_path(source_child, target / source_child.name) for source_child in source_children)

    if not target.is_file():
        return False
    with source.open("rb") as source_file, target.open("rb") as target_file:
        return source_file.read() == target_file.read()
