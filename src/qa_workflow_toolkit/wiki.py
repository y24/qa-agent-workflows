from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from .agents import get_agent_spec, supported_agent_ids
from .paths import asset_path
from .registry import default_wiki_type, get_wiki_type


SUPPORTED_WIKI_AGENTS = supported_agent_ids()
WIKI_OPERATIONS = ("ingest", "query", "lint", "convert")


@dataclass(frozen=True)
class WikiInitItem:
    kind: str
    target: Path
    content: str | None = None
    is_dir: bool = False

    @property
    def exists(self) -> bool:
        return self.target.exists()


@dataclass(frozen=True)
class WikiInitResult:
    created: tuple[Path, ...]
    overwritten: tuple[Path, ...]
    skipped: tuple[Path, ...]


WIKI_NAME_PATTERN = re.compile(r"<!--\s*wiki-name:\s*(.*?)\s*-->")
WIKI_HEADING_PATTERN = re.compile(r"^#\s+(.+?)\s+LLM Wiki\s*$", re.MULTILINE)


def build_wiki_init_items(
    target_dir: Path,
    wiki_name: str,
    agent: str,
    wiki_type: str | None = None,
) -> list[WikiInitItem]:
    if agent not in SUPPORTED_WIKI_AGENTS:
        raise ValueError(f"unsupported wiki agent: {agent}")
    resolved_wiki_type = resolve_wiki_type(wiki_type)

    agent_spec = get_agent_spec(agent)
    items = [
        WikiInitItem(
            "agents_md",
            target_dir / "AGENTS.md",
            _template("wiki/AGENTS.md", wiki_name=wiki_name, wiki_type=resolved_wiki_type.id),
        ),
        WikiInitItem("raw_dir", target_dir / "raw", is_dir=True),
        WikiInitItem("wiki_dir", target_dir / "wiki", is_dir=True),
    ]
    for subdir in resolved_wiki_type.wiki_subdirs:
        items.append(WikiInitItem(f"wiki_{subdir}_dir", target_dir / "wiki" / subdir, is_dir=True))
    items.extend(
        [
            WikiInitItem("temp_dir", target_dir / ".temp", is_dir=True),
            WikiInitItem("raw_keep", target_dir / "raw" / ".gitkeep", ""),
            WikiInitItem("wiki_keep", target_dir / "wiki" / ".gitkeep", ""),
        ]
    )
    for subdir in resolved_wiki_type.wiki_subdirs:
        items.append(WikiInitItem(f"wiki_{subdir}_keep", target_dir / "wiki" / subdir / ".gitkeep", ""))
    items.extend(
        [
            WikiInitItem("temp_keep", target_dir / ".temp" / ".gitkeep", ""),
            WikiInitItem("index", target_dir / "index.md", _template("wiki/index.md", wiki_name=wiki_name, wiki_type=resolved_wiki_type.id)),
            WikiInitItem("log", target_dir / "log.md", _template("wiki/log.md", wiki_type=resolved_wiki_type.id)),
        ]
    )
    for operation in WIKI_OPERATIONS:
        items.append(
            WikiInitItem(
                "command",
                target_dir / agent_spec.command_target_dir / agent_spec.command_filename(operation),
                _template(f"wiki/commands/{operation}.md", wiki_type=resolved_wiki_type.id),
            )
        )
    return items


def build_wiki_update_items(
    target_dir: Path,
    wiki_name: str,
    agent: str,
    wiki_type: str | None = None,
) -> list[WikiInitItem]:
    if agent not in SUPPORTED_WIKI_AGENTS:
        raise ValueError(f"unsupported wiki agent: {agent}")
    resolved_wiki_type = resolve_wiki_type(wiki_type)

    agent_spec = get_agent_spec(agent)
    items = [
        WikiInitItem(
            "agents_md",
            target_dir / "AGENTS.md",
            _template("wiki/AGENTS.md", wiki_name=wiki_name, wiki_type=resolved_wiki_type.id),
        ),
    ]
    for operation in WIKI_OPERATIONS:
        items.append(
            WikiInitItem(
                "command",
                target_dir / agent_spec.command_target_dir / agent_spec.command_filename(operation),
                _template(f"wiki/commands/{operation}.md", wiki_type=resolved_wiki_type.id),
            )
        )
    return items


def resolve_wiki_type(wiki_type: str | None):
    try:
        return get_wiki_type(wiki_type) if wiki_type else default_wiki_type()
    except KeyError as exc:
        raise ValueError(f"unsupported wiki type: {wiki_type}") from exc


def wiki_item_matches_target(item: WikiInitItem) -> bool:
    if item.is_dir:
        return item.target.is_dir()
    return item.target.is_file() and item.target.read_text(encoding="utf-8") == (item.content or "")


def init_wiki_from_items(
    items: list[WikiInitItem],
    overwrite: bool,
    overwrite_targets: set[Path] | None = None,
) -> WikiInitResult:
    overwrite_targets = overwrite_targets or set()
    created: list[Path] = []
    overwritten: list[Path] = []
    skipped: list[Path] = []

    for item in items:
        if item.is_dir:
            if item.target.exists():
                skipped.append(item.target)
            else:
                item.target.mkdir(parents=True, exist_ok=True)
                created.append(item.target)
            continue

        should_overwrite = overwrite or item.target in overwrite_targets
        if item.target.exists() and not should_overwrite:
            skipped.append(item.target)
            continue

        item.target.parent.mkdir(parents=True, exist_ok=True)
        existed = item.target.exists()
        item.target.write_text(item.content or "", encoding="utf-8")
        if existed:
            overwritten.append(item.target)
        else:
            created.append(item.target)

    return WikiInitResult(created=tuple(created), overwritten=tuple(overwritten), skipped=tuple(skipped))


def resolve_existing_wiki_name(target_dir: Path) -> str:
    agents_md = target_dir / "AGENTS.md"
    if agents_md.is_file():
        content = agents_md.read_text(encoding="utf-8")
        metadata_match = WIKI_NAME_PATTERN.search(content)
        if metadata_match and metadata_match.group(1).strip():
            return metadata_match.group(1).strip()
        heading_match = WIKI_HEADING_PATTERN.search(content)
        if heading_match and heading_match.group(1).strip():
            return heading_match.group(1).strip()
    return target_dir.name or "llm-wiki"


def is_wiki_initialized(target_dir: Path) -> bool:
    agents_md = target_dir / "AGENTS.md"
    if agents_md.is_file():
        content = agents_md.read_text(encoding="utf-8")
        if "wiki-name:" in content or "LLM Wiki" in content:
            return True
    if any(
        (target_dir / get_agent_spec(agent).command_target_dir / get_agent_spec(agent).command_filename("ingest")).is_file()
        for agent in SUPPORTED_WIKI_AGENTS
    ):
        return True
    return (target_dir / "wiki").is_dir() and (target_dir / "raw").is_dir()


def _template(relative_path: str, wiki_type: str, **replacements: str) -> str:
    template_path = _wiki_template_path(relative_path, wiki_type)
    if not template_path.is_file():
        raise FileNotFoundError(f"wiki template not found for type '{wiki_type}': {relative_path}")

    content = template_path.read_text(encoding="utf-8")
    replacements = {"wiki_type": wiki_type, **replacements}
    for key, value in replacements.items():
        content = content.replace(f"[[{key}]]", value)
    return content


def _wiki_template_path(relative_path: str, wiki_type: str):
    return asset_path(f"wiki/types/{wiki_type}/{relative_path.removeprefix('wiki/')}")
