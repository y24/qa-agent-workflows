from __future__ import annotations

from rich.console import Console
from rich.table import Table

from . import __version__
from .models import InstallPlanItem, WorkflowManifest

console = Console()


def print_header() -> None:
    console.print(f"[bold]QA Workflow Toolkit {__version__}[/bold]")
    console.print("CLI installer for QA agent workflow assets.\n")


def print_usage() -> None:
    print_header()
    console.print("[bold]Usage[/bold]")
    console.print("  qatool install    Install QA workflow assets into current folder")
    console.print("  qatool list       Show available workflows\n")
    console.print("[bold]Examples[/bold]")
    console.print("  qatool install")
    console.print("  qatool install --workflow test-design --agent roocode --yes")
    console.print("  qatool install --workflow all --agent roocode --yes")


def print_workflow_table(workflows: list[WorkflowManifest]) -> None:
    table = Table(title="Available workflows")
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    table.add_column("Description")
    table.add_column("Agents")
    for workflow in workflows:
        table.add_row(
            workflow.id,
            workflow.display_name,
            workflow.description,
            ", ".join(workflow.supported_agents),
        )
    console.print(table)


def print_plan(plan: list[InstallPlanItem]) -> None:
    table = Table(title="Install plan")
    table.add_column("Kind")
    table.add_column("Target")
    table.add_column("Exists")
    table.add_column("Action")
    for item in plan:
        table.add_row(item.kind, str(item.target), "yes" if item.exists else "no", item.action.value if item.action else "")
    console.print(table)
