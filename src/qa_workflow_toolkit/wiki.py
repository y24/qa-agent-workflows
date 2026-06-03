from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from .agents import get_agent_spec, supported_agent_ids
from .paths import asset_path


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


def build_wiki_init_items(target_dir: Path, wiki_name: str, agent: str) -> list[WikiInitItem]:
    if agent not in SUPPORTED_WIKI_AGENTS:
        raise ValueError(f"unsupported wiki agent: {agent}")

    agent_spec = get_agent_spec(agent)
    items = [
        WikiInitItem("agents_md", target_dir / "AGENTS.md", _template("wiki/AGENTS.md", wiki_name=wiki_name)),
        WikiInitItem("raw_dir", target_dir / "raw", is_dir=True),
        WikiInitItem("wiki_dir", target_dir / "wiki", is_dir=True),
        WikiInitItem("wiki_articles_dir", target_dir / "wiki" / "articles", is_dir=True),
        WikiInitItem("wiki_concepts_dir", target_dir / "wiki" / "concepts", is_dir=True),
        WikiInitItem("wiki_queries_dir", target_dir / "wiki" / "queries", is_dir=True),
        WikiInitItem("temp_dir", target_dir / ".temp", is_dir=True),
        WikiInitItem("raw_keep", target_dir / "raw" / ".gitkeep", ""),
        WikiInitItem("wiki_keep", target_dir / "wiki" / ".gitkeep", ""),
        WikiInitItem("wiki_articles_keep", target_dir / "wiki" / "articles" / ".gitkeep", ""),
        WikiInitItem("wiki_concepts_keep", target_dir / "wiki" / "concepts" / ".gitkeep", ""),
        WikiInitItem("wiki_queries_keep", target_dir / "wiki" / "queries" / ".gitkeep", ""),
        WikiInitItem("temp_keep", target_dir / ".temp" / ".gitkeep", ""),
        WikiInitItem("index", target_dir / "index.md", _template("wiki/index.md", wiki_name=wiki_name)),
        WikiInitItem("log", target_dir / "log.md", _template("wiki/log.md")),
    ]
    for operation in WIKI_OPERATIONS:
        items.append(
            WikiInitItem(
                "command",
                target_dir / agent_spec.command_target_dir / agent_spec.command_filename(operation),
                _template(f"wiki/commands/{operation}.md"),
            )
        )
    return items


def build_wiki_update_items(target_dir: Path, wiki_name: str, agent: str) -> list[WikiInitItem]:
    if agent not in SUPPORTED_WIKI_AGENTS:
        raise ValueError(f"unsupported wiki agent: {agent}")

    agent_spec = get_agent_spec(agent)
    items = [
        WikiInitItem("agents_md", target_dir / "AGENTS.md", _template("wiki/AGENTS.md", wiki_name=wiki_name)),
    ]
    for operation in WIKI_OPERATIONS:
        items.append(
            WikiInitItem(
                "command",
                target_dir / agent_spec.command_target_dir / agent_spec.command_filename(operation),
                _template(f"wiki/commands/{operation}.md"),
            )
        )
    return items


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


def _template(relative_path: str, **replacements: str) -> str:
    template_path = asset_path(relative_path)
    if not template_path.is_file():
        raise FileNotFoundError(f"wiki template not found: {relative_path}")

    content = template_path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        content = content.replace(f"[[{key}]]", value)
    return content
