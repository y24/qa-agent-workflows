from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from .agents import get_agent_spec
from .console import (
    console,
    print_header,
    print_plan,
    print_uninstall_plan,
    print_usage,
    print_wiki_init_plan,
    print_wiki_update_plan,
    print_workflow_list,
)
from .installer import (
    apply_default_actions,
    build_install_plan,
    build_uninstall_plan,
    install_from_plan,
    uninstall_from_plan,
)
from .models import CollisionAction, InstallPlanItem, UninstallPlanItem, WorkflowManifest
from .registry import get_workflow, load_workflows
from .state import (
    AGENTS_MD_KIND_WIKI,
    InstalledWorkflow,
    RepositoryConfig,
    load_installed_workflows,
    load_repository_config,
    record_installed_workflows,
    record_repository_config,
    remove_installed_workflows,
)
from .wiki import (
    SUPPORTED_WIKI_AGENTS,
    WIKI_OPERATIONS,
    build_wiki_init_items,
    build_wiki_update_items,
    init_wiki_from_items,
    is_wiki_initialized,
    resolve_existing_wiki_name,
    wiki_item_matches_target,
)

app = typer.Typer(invoke_without_command=True, no_args_is_help=False, add_completion=False)
workflow_app = typer.Typer(help="Manage QA workflow assets.", no_args_is_help=True, add_completion=False)
wiki_app = typer.Typer(help="Manage LLM wiki assets.", no_args_is_help=True, add_completion=False)
app.add_typer(workflow_app, name="workflow")
app.add_typer(wiki_app, name="wiki")


@app.callback()
def callback(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        _interactive_menu()
        raise typer.Exit()


@wiki_app.command("init")
def init_wiki(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Wiki name. Defaults to the target folder name."),
    agent: Optional[str] = typer.Option(None, "--agent", "-a", help="Target agent."),
    target: Path = typer.Option(Path.cwd(), "--target", "-t", help="Target wiki directory."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Overwrite existing generated files without prompting."),
) -> None:
    """Initialize an LLM wiki in a project."""
    _run_wiki_init(name=name, agent=agent, target=target, yes=yes, show_header=True)


@wiki_app.command("update")
def update_wiki(
    target: Path = typer.Option(Path.cwd(), "--target", "-t", help="Target wiki directory."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Apply updates without prompting."),
    agents_md: Optional[bool] = typer.Option(
        None,
        "--agents-md/--no-agents-md",
        help="Update AGENTS.md. If omitted, update it when this target was initialized as a wiki.",
    ),
) -> None:
    """Update installed LLM wiki assets in a project."""
    _run_wiki_update(target=target, yes=yes, agents_md=agents_md, show_header=True)


def _run_wiki_init(
    name: Optional[str],
    agent: Optional[str],
    target: Path,
    yes: bool,
    show_header: bool,
) -> None:
    if show_header:
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
    record_repository_config(resolved_target, selected_agent, include_agents_md=False, agents_md_kind=AGENTS_MD_KIND_WIKI)
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


def _run_wiki_update(
    target: Path,
    yes: bool,
    agents_md: Optional[bool],
    show_header: bool,
) -> None:
    if show_header:
        print_header()
    resolved_target = target.resolve()
    repository_config = load_repository_config(resolved_target)
    if not _has_installed_wiki(resolved_target, repository_config):
        console.print("[yellow]No initialized wiki assets were found.[/yellow]")
        raise typer.Exit(1)

    selected_agent = _resolve_wiki_update_agent(yes, resolved_target, repository_config)
    wiki_name = resolve_existing_wiki_name(resolved_target)
    include_agents_md = agents_md if agents_md is not None else _should_update_wiki_agents_md(repository_config)
    plan = build_wiki_update_items(resolved_target, wiki_name, selected_agent)
    if not include_agents_md:
        plan = [item for item in plan if item.kind != "agents_md"]
    plan = [item for item in plan if not wiki_item_matches_target(item)]

    if not plan:
        console.print("[green]No updates available.[/green]")
        return
    print_wiki_update_plan(plan)
    if not yes and not _questionary().confirm("Update these wiki files?", default=True).ask():
        raise typer.Exit(1)

    result = init_wiki_from_items(plan, overwrite=True)
    record_repository_config(
        resolved_target,
        selected_agent,
        include_agents_md=False,
        agents_md_kind=AGENTS_MD_KIND_WIKI if include_agents_md else (repository_config.agents_md_kind if repository_config else None),
    )
    console.print(f"\n[green]Updated {len(result.created) + len(result.overwritten)} item(s).[/green]")
    if result.skipped:
        console.print(f"[yellow]Skipped {len(result.skipped)} item(s).[/yellow]")


@workflow_app.command("list")
def list_workflows() -> None:
    """Show available workflows."""
    _run_workflow_list(show_header=True)


def _run_workflow_list(show_header: bool) -> None:
    if show_header:
        print_header()
    print_workflow_list(load_workflows())


@workflow_app.command()
def install(
    workflow: Optional[str] = typer.Option(None, "--workflow", "-w", help="Workflow ID to install, or 'all'."),
    agent: Optional[str] = typer.Option(None, "--agent", "-a", help="Target agent."),
    target: Path = typer.Option(Path.cwd(), "--target", "-t", help="Target project directory."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Overwrite existing files without prompting."),
) -> None:
    """Install QA workflow assets into a project."""
    _run_workflow_install(workflow=workflow, agent=agent, target=target, yes=yes, show_header=True)


def _run_workflow_install(
    workflow: Optional[str],
    agent: Optional[str],
    target: Path,
    yes: bool,
    show_header: bool,
) -> None:
    if show_header:
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

    plan = _dedupe_plan(
        item
        for selected_workflow in selected_workflows
        for item in build_install_plan(selected_workflow, resolved_target, selected_agent)
    )
    if yes:
        plan = apply_default_actions(plan, CollisionAction.OVERWRITE)
    else:
        plan = [_resolve_collision(item) for item in plan]

    print_plan(plan)
    if not yes and not _questionary().confirm("Install these files?", default=True).ask():
        raise typer.Exit(1)

    result = install_from_plan(plan)
    record_installed_workflows(resolved_target, selected_workflows, selected_agent)
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
) -> None:
    """Update installed QA workflow assets in a project."""
    _run_workflow_update(workflow=workflow, target=target, yes=yes, show_header=True)


def _run_workflow_update(
    workflow: Optional[str],
    target: Path,
    yes: bool,
    show_header: bool,
) -> None:
    if show_header:
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
        for item in build_install_plan(selected_workflow, resolved_target, metadata.agent)
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
    _run_workflow_uninstall(workflow=workflow, agent=agent, target=target, yes=yes, show_header=True)


def _run_workflow_uninstall(
    workflow: Optional[str],
    agent: Optional[str],
    target: Path,
    yes: bool,
    show_header: bool,
) -> None:
    if show_header:
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


def _interactive_menu() -> None:
    print_header()
    questionary = _questionary()
    selected_command = questionary.select(
        "Select command",
        choices=[
            questionary.Choice("workflow - QA workflow skills のインストール、更新、削除", value="workflow"),
            questionary.Choice("wiki - LLM wiki の構築", value="wiki"),
            questionary.Choice("help - 利用できるコマンドと実行例を表示", value="help"),
        ],
    ).ask()
    if not selected_command:
        raise typer.Exit(1)

    if selected_command == "workflow":
        _interactive_workflow_menu(questionary)
        return
    if selected_command == "wiki":
        _interactive_wiki_menu(questionary)
        return
    print_usage(show_header=False)


def _interactive_workflow_menu(questionary) -> None:
    has_installed_workflows = _has_installed_workflow_assets(Path.cwd().resolve())
    choices = [
        questionary.Choice("install - QA workflow skills をカレントディレクトリへ配置", value="install"),
    ]
    if has_installed_workflows:
        choices.extend(
            [
                questionary.Choice("update - インストール済みの workflow skills を最新版に更新", value="update"),
                questionary.Choice("uninstall - インストール済みの workflow skills を削除", value="uninstall"),
            ]
        )
    choices.extend(
        [
            questionary.Choice("list - 利用可能な workflow 一覧を表示", value="list"),
            questionary.Choice("help - workflow コマンドのヘルプを表示", value="help"),
        ]
    )
    selected_operation = questionary.select(
        "Select workflow operation",
        choices=choices,
    ).ask()
    if not selected_operation:
        raise typer.Exit(1)

    if selected_operation == "install":
        _run_workflow_install(workflow=None, agent=None, target=Path.cwd(), yes=False, show_header=False)
    elif selected_operation == "update":
        _run_workflow_update(workflow=None, target=Path.cwd(), yes=False, show_header=False)
    elif selected_operation == "uninstall":
        _run_workflow_uninstall(workflow=None, agent=None, target=Path.cwd(), yes=False, show_header=False)
    elif selected_operation == "list":
        _run_workflow_list(show_header=False)
    else:
        print_usage(show_header=False)


def _interactive_wiki_menu(questionary) -> None:
    has_installed_wiki = _has_installed_wiki(Path.cwd().resolve(), load_repository_config(Path.cwd().resolve()))
    choices = [
        questionary.Choice("init - 現在のフォルダに LLM wiki assets を初期化", value="init"),
    ]
    if has_installed_wiki:
        choices.append(questionary.Choice("update - 初期化済みの LLM wiki assets を最新版に更新", value="update"))
    choices.append(questionary.Choice("help - wiki コマンドのヘルプを表示", value="help"))
    selected_operation = questionary.select(
        "Select wiki operation",
        choices=choices,
    ).ask()
    if not selected_operation:
        raise typer.Exit(1)

    if selected_operation == "init":
        _run_wiki_init(name=None, agent=None, target=Path.cwd(), yes=False, show_header=False)
    elif selected_operation == "update":
        _run_wiki_update(target=Path.cwd(), yes=False, agents_md=None, show_header=False)
    else:
        print_usage(show_header=False)


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


def _resolve_wiki_update_agent(yes: bool, target: Path, repository_config: RepositoryConfig | None = None) -> str:
    if repository_config is not None and repository_config.agent in SUPPORTED_WIKI_AGENTS:
        return repository_config.agent

    detected_agents = [
        agent
        for agent in SUPPORTED_WIKI_AGENTS
        if any(
            (target / get_agent_spec(agent).command_target_dir / get_agent_spec(agent).command_filename(operation)).is_file()
            for operation in WIKI_OPERATIONS
        )
    ]
    if len(detected_agents) == 1:
        return detected_agents[0]
    return _resolve_wiki_agent(yes, repository_config)


def _should_update_wiki_agents_md(repository_config: RepositoryConfig | None) -> bool:
    if repository_config is None:
        return True
    return repository_config.agents_md_kind == AGENTS_MD_KIND_WIKI


def _has_installed_wiki(target: Path, repository_config: RepositoryConfig | None) -> bool:
    return (repository_config is not None and repository_config.agents_md_kind == AGENTS_MD_KIND_WIKI) or is_wiki_initialized(target)


def _has_installed_workflow_assets(target: Path) -> bool:
    return bool(load_installed_workflows(target)) or bool(_installed_workflows(load_workflows(), target))


def _resolve_wiki_init_overwrites(plan: list, yes: bool) -> set[Path]:
    if yes:
        return set()

    agents_md = next((item for item in plan if item.kind == "agents_md"), None)
    if agents_md is None or not agents_md.target.exists():
        return set()

    selected = _questionary().confirm(
        f"{agents_md.target} already exists. Overwrite it with LLM wiki AGENTS.md?",
        default=True,
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
            include_agents_md=False,
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
