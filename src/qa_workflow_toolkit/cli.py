from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from .console import console, print_header, print_plan, print_uninstall_plan, print_usage, print_wiki_init_plan, print_workflow_list
from .installer import (
    apply_default_actions,
    asset_matches_path,
    build_install_plan,
    build_uninstall_plan,
    install_from_plan,
    uninstall_from_plan,
)
from .models import CollisionAction, InstallPlanItem, UninstallPlanItem, WorkflowManifest
from .registry import get_workflow, load_workflows
from .state import (
    InstalledWorkflow,
    RepositoryConfig,
    load_installed_workflows,
    load_repository_config,
    record_installed_workflows,
    record_repository_config,
    remove_installed_workflows,
)
from .wiki import SUPPORTED_WIKI_AGENTS, build_wiki_init_items, init_wiki_from_items

app = typer.Typer(invoke_without_command=True, no_args_is_help=False, add_completion=False)
workflow_app = typer.Typer(help="Manage QA workflow assets.", no_args_is_help=True, add_completion=False)
wiki_app = typer.Typer(help="Manage LLM wiki assets.", no_args_is_help=True, add_completion=False)
app.add_typer(workflow_app, name="workflow")
app.add_typer(wiki_app, name="wiki")


@app.callback()
def callback(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        print_usage()


@wiki_app.command("init")
def init_wiki(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Wiki name. Defaults to the target folder name."),
    agent: Optional[str] = typer.Option(None, "--agent", "-a", help="Target agent."),
    target: Path = typer.Option(Path.cwd(), "--target", "-t", help="Target wiki directory."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Overwrite existing generated files without prompting."),
) -> None:
    """Initialize an LLM wiki in a project."""
    print_header()
    resolved_target = target.resolve()
    wiki_name = name or _resolve_wiki_name(resolved_target, yes)
    repository_config = load_repository_config(resolved_target)
    selected_agent = agent or _resolve_wiki_agent(yes, repository_config)
    if selected_agent not in SUPPORTED_WIKI_AGENTS:
        raise typer.BadParameter(f"unsupported agent: {selected_agent}")
    plan = build_wiki_init_items(resolved_target, wiki_name, selected_agent)
    overwrite = yes
    overwrite_targets = _resolve_wiki_init_overwrites(plan, yes)

    print_wiki_init_plan(plan, overwrite=overwrite, overwrite_targets=overwrite_targets)
    if not yes and not _questionary().confirm("Initialize this LLM wiki?", default=True).ask():
        raise typer.Exit(1)

    result = init_wiki_from_items(plan, overwrite=overwrite, overwrite_targets=overwrite_targets)
    record_repository_config(resolved_target, selected_agent)
    console.print(f"\n[green]Created {len(result.created)} item(s).[/green]")
    if result.overwritten:
        console.print(f"[yellow]Overwritten {len(result.overwritten)} item(s).[/yellow]")
    if result.skipped:
        console.print(f"[yellow]Skipped {len(result.skipped)} existing item(s).[/yellow]")
    console.print("Usage:")
    console.print("/convert .temp/<file>")
    console.print("/ingest raw/<file>.md")
    console.print("/query <質問>")
    console.print("/lint")


@workflow_app.command("list")
def list_workflows() -> None:
    """Show available workflows."""
    print_header()
    print_workflow_list(load_workflows())


@workflow_app.command()
def install(
    workflow: Optional[str] = typer.Option(None, "--workflow", "-w", help="Workflow ID to install, or 'all'."),
    agent: Optional[str] = typer.Option(None, "--agent", "-a", help="Target agent."),
    target: Path = typer.Option(Path.cwd(), "--target", "-t", help="Target project directory."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Overwrite existing files without prompting."),
    agents_md: Optional[bool] = typer.Option(
        None,
        "--agents-md/--no-agents-md",
        help="Create AGENTS.md. If omitted in interactive mode, ask before installing.",
    ),
) -> None:
    """Install QA workflow assets into a project."""
    print_header()
    workflows = load_workflows()
    selected_workflow_id = workflow or _select_workflow(workflows)
    selected_workflows = workflows if selected_workflow_id == "all" else [get_workflow(selected_workflow_id)]
    default_agent = selected_workflows[0].default_agent
    supported_agents = tuple(sorted(set.intersection(*(set(item.supported_agents) for item in selected_workflows))))
    resolved_target = target.resolve()
    installed_metadata = load_installed_workflows(resolved_target)
    repository_config = load_repository_config(resolved_target)
    selected_agent = agent or _resolve_agent_choice(
        installed_metadata,
        selected_workflows,
        supported_agents,
        default_agent,
        repository_config,
    )
    include_agents_md = _resolve_agents_md_choice(agents_md, yes, resolved_target, selected_agent, installed_metadata, selected_workflows)

    plan = _dedupe_plan(
        item
        for selected_workflow in selected_workflows
        for item in build_install_plan(
            selected_workflow,
            resolved_target,
            selected_agent,
            include_agents_md=include_agents_md,
        )
    )
    if yes:
        plan = apply_default_actions(plan, CollisionAction.OVERWRITE)
    else:
        plan = [_resolve_collision(item) for item in plan]

    print_plan(plan)
    if not yes and not _questionary().confirm("Install these files?", default=True).ask():
        raise typer.Exit(1)

    result = install_from_plan(plan)
    record_installed_workflows(resolved_target, selected_workflows, selected_agent, include_agents_md)
    console.print(f"\n[green]Installed {len(result.copied)} item(s).[/green]")
    if result.skipped:
        console.print(f"[yellow]Skipped {len(result.skipped)} item(s).[/yellow]")
    if selected_workflow_id == "all":
        console.print("Usage:")
        for selected_workflow in selected_workflows:
            console.print(f"/{selected_workflow.command_name} <入力資料>")
    else:
        console.print("Usage:")
        console.print(selected_workflows[0].post_install_message)


@workflow_app.command()
def update(
    workflow: Optional[str] = typer.Option(None, "--workflow", "-w", help="Installed workflow ID to update, or 'all'."),
    target: Path = typer.Option(Path.cwd(), "--target", "-t", help="Target project directory."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Apply updates without prompting."),
    agents_md: Optional[bool] = typer.Option(
        None,
        "--agents-md/--no-agents-md",
        help="Update AGENTS.md. If omitted in interactive mode, ask before updating.",
    ),
) -> None:
    """Update installed QA workflow assets in a project."""
    print_header()
    workflows = load_workflows()
    resolved_target = target.resolve()
    selected_workflow_id = workflow or "all"
    installed_metadata = _installed_workflow_metadata(workflows, resolved_target)
    selected_metadata = (
        list(installed_metadata.values())
        if selected_workflow_id == "all"
        else [_require_installed_metadata(get_workflow(selected_workflow_id), installed_metadata)]
    )
    if not selected_metadata:
        console.print("[yellow]No installed workflow assets were found.[/yellow]")
        raise typer.Exit(1)

    plan = _dedupe_plan(
        item
        for metadata in selected_metadata
        for selected_workflow in [get_workflow(metadata.workflow_id)]
        for item in build_install_plan(
            selected_workflow,
            resolved_target,
            metadata.agent,
            include_agents_md=metadata.include_agents_md if agents_md is None else agents_md,
        )
    )
    plan = apply_default_actions(plan, CollisionAction.OVERWRITE)
    plan = [item for item in plan if item.action != CollisionAction.NO_CHANGE]

    if not plan:
        console.print("[green]No updates available.[/green]")
        return
    print_plan(plan)
    if not yes and not _questionary().confirm("Update these files?", default=True).ask():
        raise typer.Exit(1)

    result = install_from_plan(plan)
    for metadata in selected_metadata:
        record_installed_workflows(
            resolved_target,
            [get_workflow(metadata.workflow_id)],
            metadata.agent,
            metadata.include_agents_md if agents_md is None else agents_md,
        )
    console.print(f"\n[green]Updated {len(result.copied)} item(s).[/green]")
    if result.skipped:
        console.print(f"[yellow]Skipped {len(result.skipped)} item(s).[/yellow]")


@workflow_app.command()
def uninstall(
    workflow: Optional[str] = typer.Option(None, "--workflow", "-w", help="Installed workflow ID to uninstall, or 'all'."),
    agent: Optional[str] = typer.Option(None, "--agent", "-a", help="Target agent."),
    target: Path = typer.Option(Path.cwd(), "--target", "-t", help="Target project directory."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Remove matching generated assets without prompting."),
) -> None:
    """Uninstall QA workflow assets from a project."""
    print_header()
    workflows = load_workflows()
    resolved_target = target.resolve()
    installed_workflows = _installed_workflows(workflows, resolved_target)
    if not installed_workflows:
        console.print("[yellow]No installed workflow assets were found.[/yellow]")
        raise typer.Exit(1)

    selected_workflow_id = workflow or _select_installed_workflow(installed_workflows)
    installed_metadata = _installed_workflow_metadata(workflows, resolved_target)
    selected_workflows = (
        installed_workflows if selected_workflow_id == "all" else [_require_installed(get_workflow(selected_workflow_id), resolved_target)]
    )
    selected_metadata = [_require_installed_metadata(selected_workflow, installed_metadata) for selected_workflow in selected_workflows]
    include_common_assets = {workflow.id for workflow in selected_workflows} == {workflow.id for workflow in installed_workflows}

    plan = _dedupe_uninstall_plan(
        item
        for index, metadata in enumerate(selected_metadata)
        for selected_workflow in [get_workflow(metadata.workflow_id)]
        for item in build_uninstall_plan(
            selected_workflow,
            resolved_target,
            agent or metadata.agent,
            include_shared=include_common_assets and index == 0,
            include_agents_md=metadata.include_agents_md and include_common_assets and index == 0,
        )
    )
    print_uninstall_plan(plan)
    if not yes and not _questionary().confirm("Remove these files? Modified files are skipped.", default=True).ask():
        raise typer.Exit(1)

    result = uninstall_from_plan(plan)
    remove_installed_workflows(
        resolved_target,
        [workflow.id for workflow in selected_workflows if not _is_workflow_installed(workflow, resolved_target)],
    )
    console.print(f"\n[green]Removed {len(result.removed)} item(s).[/green]")
    if result.skipped:
        console.print(f"[yellow]Skipped {len(result.skipped)} item(s).[/yellow]")


def _resolve_wiki_name(target: Path, yes: bool) -> str:
    default_name = target.name or "llm-wiki"
    if yes:
        return default_name
    selected = _questionary().text("Wiki name", default=default_name).ask()
    if selected is None:
        raise typer.Exit(1)
    return str(selected).strip() or default_name


def _resolve_wiki_agent(yes: bool, repository_config: RepositoryConfig | None = None) -> str:
    default_agent = SUPPORTED_WIKI_AGENTS[0]
    if repository_config is not None and repository_config.agent in SUPPORTED_WIKI_AGENTS:
        return repository_config.agent
    if yes:
        return default_agent
    return _select_agent(SUPPORTED_WIKI_AGENTS, default_agent)


def _resolve_wiki_init_overwrites(plan: list, yes: bool) -> set[Path]:
    if yes:
        return set()

    agents_md = next((item for item in plan if item.kind == "agents_md"), None)
    if agents_md is None or not agents_md.target.exists():
        return set()

    selected = _questionary().confirm(
        f"{agents_md.target} already exists. Overwrite it with LLM wiki AGENTS.md?",
        default=False,
    ).ask()
    if selected is None:
        raise typer.Exit(1)
    return {agents_md.target} if selected else set()


def _select_workflow(workflows: list) -> str:
    questionary = _questionary()
    choices = [questionary.Choice("all - すべてのworkflow", value="all")]
    choices.extend(questionary.Choice(f"{workflow.id} - {workflow.display_name}", value=workflow.id) for workflow in workflows)
    selected = questionary.select("Select workflow", choices=choices).ask()
    if not selected:
        raise typer.Exit(1)
    return str(selected)


def _select_installed_workflow(workflows: list[WorkflowManifest]) -> str:
    questionary = _questionary()
    choices = [questionary.Choice("all - インストール済みのすべてのworkflow", value="all")]
    choices.extend(questionary.Choice(f"{workflow.id} - {workflow.display_name}", value=workflow.id) for workflow in workflows)
    selected = questionary.select("Select workflow to uninstall", choices=choices).ask()
    if not selected:
        raise typer.Exit(1)
    return str(selected)


def _select_agent(supported_agents: tuple[str, ...], default_agent: str) -> str:
    questionary = _questionary()
    selected = questionary.select("Select target agent", choices=list(supported_agents), default=default_agent).ask()
    if not selected:
        raise typer.Exit(1)
    return str(selected)


def _resolve_agent_choice(
    installed_metadata: dict[str, InstalledWorkflow],
    selected_workflows: list[WorkflowManifest],
    supported_agents: tuple[str, ...],
    default_agent: str,
    repository_config: RepositoryConfig | None = None,
) -> str:
    saved_agent = _saved_metadata_value(installed_metadata, selected_workflows, "agent")
    if isinstance(saved_agent, str) and saved_agent in supported_agents:
        return saved_agent
    if repository_config is not None and repository_config.agent in supported_agents:
        return repository_config.agent
    return _select_agent(supported_agents, default_agent)


def _resolve_agents_md_choice(
    agents_md: Optional[bool],
    yes: bool,
    target: Path,
    agent: str,
    installed_metadata: dict[str, InstalledWorkflow] | None = None,
    selected_workflows: list[WorkflowManifest] | None = None,
) -> bool:
    if agents_md is not None:
        return agents_md
    if installed_metadata is not None and selected_workflows is not None:
        saved_include_agents_md = _saved_metadata_value(installed_metadata, selected_workflows, "include_agents_md")
        if isinstance(saved_include_agents_md, bool):
            return saved_include_agents_md
    if yes:
        return True
    if asset_matches_path(f"agents/{agent}/AGENTS.md", target / "AGENTS.md"):
        return True

    selected = _questionary().confirm(
        "Create AGENTS.md? Choose No if you want to keep the target repository's existing agent instructions unchanged.",
        default=True,
    ).ask()
    if selected is None:
        raise typer.Exit(1)
    return bool(selected)


def _saved_metadata_value(
    installed_metadata: dict[str, InstalledWorkflow],
    selected_workflows: list[WorkflowManifest],
    field_name: str,
) -> object | None:
    selected_workflow_ids = {workflow.id for workflow in selected_workflows}
    selected_values = {
        getattr(metadata, field_name)
        for workflow_id, metadata in installed_metadata.items()
        if workflow_id in selected_workflow_ids
    }
    if len(selected_values) == 1:
        return next(iter(selected_values))

    repo_values = {getattr(metadata, field_name) for metadata in installed_metadata.values()}
    if len(repo_values) == 1:
        return next(iter(repo_values))
    return None


def _resolve_collision(item: InstallPlanItem) -> InstallPlanItem:
    questionary = _questionary()
    if item.action == CollisionAction.NO_CHANGE:
        return item
    if not item.exists:
        return InstallPlanItem(item.kind, item.source, item.target, item.exists, item.is_dir, CollisionAction.OVERWRITE)

    if item.kind == "agents_md":
        action = questionary.select(
            f"{item.target} already exists",
            choices=[
                questionary.Choice("Overwrite", CollisionAction.OVERWRITE),
                questionary.Choice("Rename", CollisionAction.RENAME),
                questionary.Choice("Skip", CollisionAction.SKIP),
            ],
        ).ask()
    else:
        action = questionary.select(
            f"{item.target} already exists",
            choices=[
                questionary.Choice("Overwrite", CollisionAction.OVERWRITE),
                questionary.Choice("Skip", CollisionAction.SKIP),
            ],
        ).ask()

    if not action:
        raise typer.Exit(1)
    return InstallPlanItem(item.kind, item.source, item.target, item.exists, item.is_dir, action)


def _dedupe_plan(items) -> list[InstallPlanItem]:
    deduped: list[InstallPlanItem] = []
    seen: set[Path] = set()
    for item in items:
        key = item.target
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def _dedupe_uninstall_plan(items) -> list[UninstallPlanItem]:
    deduped: list[UninstallPlanItem] = []
    seen: set[Path] = set()
    for item in items:
        key = item.target
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def _installed_workflows(workflows: list[WorkflowManifest], target: Path) -> list[WorkflowManifest]:
    return [workflow for workflow in workflows if _is_workflow_installed(workflow, target)]


def _installed_workflow_metadata(workflows: list[WorkflowManifest], target: Path) -> dict[str, InstalledWorkflow]:
    metadata = load_installed_workflows(target)
    if metadata:
        return metadata
    return {
        workflow.id: InstalledWorkflow(
            workflow_id=workflow.id,
            agent=workflow.default_agent,
            include_agents_md=(target / "AGENTS.md").exists(),
            manifest_version=workflow.version,
            installed_at="",
            updated_at="",
        )
        for workflow in _installed_workflows(workflows, target)
    }


def _require_installed_metadata(
    workflow: WorkflowManifest,
    metadata: dict[str, InstalledWorkflow],
) -> InstalledWorkflow:
    installed = metadata.get(workflow.id)
    if not installed:
        raise typer.BadParameter(f"workflow is not installed: {workflow.id}")
    return installed


def _require_installed(workflow: WorkflowManifest, target: Path) -> WorkflowManifest:
    if not _is_workflow_installed(workflow, target):
        raise typer.BadParameter(f"workflow is not installed: {workflow.id}")
    return workflow


def _is_workflow_installed(workflow: WorkflowManifest, target: Path) -> bool:
    return (target / workflow.install.skill.target / "SKILL.md").exists() or (target / workflow.install.command.target).exists()


def _questionary():
    try:
        import questionary
    except ModuleNotFoundError as exc:
        raise typer.BadParameter("questionary is required for interactive prompts. Run `pip install -e .`.") from exc
    return questionary


def main() -> None:
    app()
