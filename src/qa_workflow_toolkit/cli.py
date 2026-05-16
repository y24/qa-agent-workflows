from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from .console import console, print_header, print_plan, print_usage, print_workflow_list
from .installer import apply_default_actions, build_install_plan, install_from_plan
from .models import CollisionAction, InstallPlanItem
from .registry import get_workflow, load_workflows

app = typer.Typer(invoke_without_command=True, no_args_is_help=False, add_completion=False)


@app.callback()
def callback(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        print_usage()


@app.command("list")
def list_workflows() -> None:
    """Show available workflows."""
    print_header()
    print_workflow_list(load_workflows())


@app.command()
def install(
    workflow: Optional[str] = typer.Option(None, "--workflow", "-w", help="Workflow ID to install, or 'all'."),
    agent: Optional[str] = typer.Option(None, "--agent", "-a", help="Target agent."),
    target: Path = typer.Option(Path.cwd(), "--target", "-t", help="Target project directory."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Overwrite existing files without prompting."),
) -> None:
    """Install QA workflow assets into a project."""
    print_header()
    workflows = load_workflows()
    selected_workflow_id = workflow or _select_workflow(workflows)
    selected_workflows = workflows if selected_workflow_id == "all" else [get_workflow(selected_workflow_id)]
    default_agent = selected_workflows[0].default_agent
    supported_agents = tuple(sorted(set.intersection(*(set(item.supported_agents) for item in selected_workflows))))
    selected_agent = agent or _select_agent(supported_agents, default_agent)

    plan = _dedupe_plan(
        item
        for selected_workflow in selected_workflows
        for item in build_install_plan(selected_workflow, target.resolve(), selected_agent)
    )
    if yes:
        plan = apply_default_actions(plan, CollisionAction.OVERWRITE)
    else:
        plan = [_resolve_collision(item) for item in plan]

    print_plan(plan)
    if not yes and not _questionary().confirm("Install these files?", default=True).ask():
        raise typer.Exit(1)

    result = install_from_plan(plan)
    console.print(f"\n[green]Installed {len(result.copied)} item(s).[/green]")
    if result.skipped:
        console.print(f"[yellow]Skipped {len(result.skipped)} item(s).[/yellow]")
    if selected_workflow_id == "all":
        console.print("RooCodeで `/scenario-test-design <入力資料>` など、導入したworkflowのslash commandを実行してください。")
    else:
        console.print(selected_workflows[0].post_install_message)


def _select_workflow(workflows: list) -> str:
    questionary = _questionary()
    choices = [questionary.Choice("all - すべてのworkflow", value="all")]
    choices.extend(questionary.Choice(f"{workflow.id} - {workflow.display_name}", value=workflow.id) for workflow in workflows)
    selected = questionary.select("Select workflow", choices=choices).ask()
    if not selected:
        raise typer.Exit(1)
    return str(selected)


def _select_agent(supported_agents: tuple[str, ...], default_agent: str) -> str:
    questionary = _questionary()
    selected = questionary.select("Select target agent", choices=list(supported_agents), default=default_agent).ask()
    if not selected:
        raise typer.Exit(1)
    return str(selected)


def _resolve_collision(item: InstallPlanItem) -> InstallPlanItem:
    questionary = _questionary()
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


def _questionary():
    try:
        import questionary
    except ModuleNotFoundError as exc:
        raise typer.BadParameter("questionary is required for interactive install. Run `pip install -e .`.") from exc
    return questionary


def main() -> None:
    app()
