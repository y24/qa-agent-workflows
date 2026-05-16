from __future__ import annotations

import json

from .models import WorkflowManifest
from .paths import asset_path


def load_workflows() -> list[WorkflowManifest]:
    workflows_root = asset_path("workflows")
    manifests: list[WorkflowManifest] = []
    for workflow_dir in workflows_root.iterdir():
        if not workflow_dir.is_dir():
            continue
        manifest_path = workflow_dir / "workflow.json"
        if not manifest_path.is_file():
            continue
        with manifest_path.open("r", encoding="utf-8") as handle:
            manifests.append(WorkflowManifest.from_dict(json.load(handle)))
    return sorted(manifests, key=lambda workflow: workflow.id)


def get_workflow(workflow_id: str) -> WorkflowManifest:
    for workflow in load_workflows():
        if workflow.id == workflow_id:
            return workflow
    raise KeyError(f"unknown workflow: {workflow_id}")
