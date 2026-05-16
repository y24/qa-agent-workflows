from __future__ import annotations

import shutil
from pathlib import Path

from importlib.resources.abc import Traversable

from .models import CollisionAction, InstallPlanItem, InstallResult, WorkflowManifest
from .paths import asset_path


def build_install_plan(workflow: WorkflowManifest, target_dir: Path, agent: str) -> list[InstallPlanItem]:
    if agent not in workflow.supported_agents:
        raise ValueError(f"{workflow.id} does not support agent: {agent}")

    items: list[InstallPlanItem] = []
    if workflow.install.agents_md:
        items.append(_plan_item("agents_md", f"agents/{agent}/AGENTS.md", target_dir / "AGENTS.md"))

    items.append(_plan_item("shared", workflow.install.shared.source, target_dir / workflow.install.shared.target))
    items.append(_plan_item("skill", workflow.install.skill.source, target_dir / workflow.install.skill.target))
    items.append(_plan_item("command", workflow.install.command.source, target_dir / workflow.install.command.target))
    return items


def apply_default_actions(plan: list[InstallPlanItem], action: CollisionAction) -> list[InstallPlanItem]:
    return [
        InstallPlanItem(
            kind=item.kind,
            source=item.source,
            target=item.target,
            exists=item.exists,
            is_dir=item.is_dir,
            action=action if item.exists else CollisionAction.OVERWRITE,
        )
        for item in plan
    ]


def install_from_plan(plan: list[InstallPlanItem]) -> InstallResult:
    copied: list[Path] = []
    skipped: list[Path] = []
    renamed: list[Path] = []

    for item in plan:
        action = item.action or (CollisionAction.SKIP if item.exists else CollisionAction.OVERWRITE)
        if item.exists and action == CollisionAction.SKIP:
            skipped.append(item.target)
            continue

        target = item.target
        if item.exists and action == CollisionAction.RENAME:
            target = next_available_agents_path(item.target)
            renamed.append(target)

        source = asset_path(item.source)
        _copy_resource(source, target, overwrite=action == CollisionAction.OVERWRITE)
        copied.append(target)

    return InstallResult(copied=tuple(copied), skipped=tuple(skipped), renamed=tuple(renamed))


def next_available_agents_path(path: Path) -> Path:
    for index in range(1, 1000):
        candidate = path.with_name(f"{path.stem}_{index}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"could not find available filename for {path}")


def _plan_item(kind: str, source: str, target: Path) -> InstallPlanItem:
    source_resource = asset_path(source)
    if not source_resource.exists():
        raise FileNotFoundError(f"asset not found: {source}")
    return InstallPlanItem(
        kind=kind,
        source=source,
        target=target,
        exists=target.exists(),
        is_dir=source_resource.is_dir(),
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
