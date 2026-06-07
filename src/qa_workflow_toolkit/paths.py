from __future__ import annotations

from importlib.resources import files
from importlib.resources.abc import Traversable

ASSET_PACKAGE = "qa_workflow_toolkit.assets"


def assets_root() -> Traversable:
    return files(ASSET_PACKAGE)


def asset_path(relative_path: str) -> Traversable:
    current = assets_root()
    for part in relative_path.replace("\\", "/").split("/"):
        if part:
            current = current / part
    return current


def workflow_asset_path(relative_path: str) -> Traversable:
    return asset_path(f"workflow/{relative_path}")


def wiki_asset_path(relative_path: str) -> Traversable:
    return asset_path(f"wiki/{relative_path}")
