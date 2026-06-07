from __future__ import annotations

import json

from .models import WikiTypeManifest, WorkflowManifest
from .paths import wiki_asset_path, workflow_asset_path


def _workflow_sort_key(workflow: WorkflowManifest) -> tuple[int, int, str]:
    if workflow.sort_order is None:
        return (1, 0, workflow.id)
    return (0, workflow.sort_order, workflow.id)


def load_workflows() -> list[WorkflowManifest]:
    workflows_root = workflow_asset_path("workflows")
    manifests: list[WorkflowManifest] = []
    for workflow_dir in workflows_root.iterdir():
        if not workflow_dir.is_dir():
            continue
        manifest_path = workflow_dir / "workflow.json"
        if not manifest_path.is_file():
            continue
        with manifest_path.open("r", encoding="utf-8") as handle:
            manifests.append(WorkflowManifest.from_dict(json.load(handle)))
    return sorted(manifests, key=_workflow_sort_key)


def get_workflow(workflow_id: str) -> WorkflowManifest:
    for workflow in load_workflows():
        if workflow.id == workflow_id:
            return workflow
    raise KeyError(f"unknown workflow: {workflow_id}")


def _wiki_type_sort_key(wiki_type: WikiTypeManifest) -> tuple[int, int, str]:
    if wiki_type.sort_order is None:
        return (1, 0, wiki_type.id)
    return (0, wiki_type.sort_order, wiki_type.id)


def load_wiki_types() -> list[WikiTypeManifest]:
    wiki_types_root = wiki_asset_path("types")
    manifests: list[WikiTypeManifest] = []
    for wiki_type_dir in wiki_types_root.iterdir():
        if not wiki_type_dir.is_dir():
            continue
        manifest_path = wiki_type_dir / "wiki_type.json"
        if not manifest_path.is_file():
            continue
        with manifest_path.open("r", encoding="utf-8") as handle:
            manifests.append(WikiTypeManifest.from_dict(json.load(handle)))
    return sorted(manifests, key=_wiki_type_sort_key)


def get_wiki_type(wiki_type_id: str) -> WikiTypeManifest:
    selected = wiki_type_id.strip().lower()
    for wiki_type in load_wiki_types():
        if wiki_type.id == selected or wiki_type.display_name.lower() == selected:
            return wiki_type
    raise KeyError(f"unknown wiki type: {wiki_type_id}")


def default_wiki_type() -> WikiTypeManifest:
    wiki_types = load_wiki_types()
    for wiki_type in wiki_types:
        if wiki_type.is_default:
            return wiki_type
    if wiki_types:
        return wiki_types[0]
    raise KeyError("no wiki types are available")
