from __future__ import annotations

from dataclasses import dataclass


DEFAULT_AGENT = "roocode"


@dataclass(frozen=True)
class AgentSpec:
    id: str
    command_target_dir: str
    command_filename_suffix: str = ".md"

    def command_filename(self, command_name: str) -> str:
        return f"{command_name}{self.command_filename_suffix}"


SUPPORTED_AGENTS: dict[str, AgentSpec] = {
    "roocode": AgentSpec(id="roocode", command_target_dir=".roo/commands"),
    "claude": AgentSpec(id="claude", command_target_dir=".claude/commands"),
    "copilot": AgentSpec(id="copilot", command_target_dir=".github/prompts", command_filename_suffix=".prompt.md"),
    "codex": AgentSpec(id="codex", command_target_dir=".codex/prompts"),
}


def supported_agent_ids() -> tuple[str, ...]:
    return tuple(SUPPORTED_AGENTS)


def get_agent_spec(agent: str) -> AgentSpec:
    try:
        return SUPPORTED_AGENTS[agent]
    except KeyError as exc:
        raise ValueError(f"unsupported agent: {agent}") from exc
