from __future__ import annotations

from rich.console import Console
from rich.markup import escape
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
    console.print("  qatool install --workflow scenario-test-design --agent roocode --yes")
    console.print("  qatool install --workflow all --agent roocode --yes")


def print_workflow_list(workflows: list[WorkflowManifest]) -> None:
    console.print("[bold]Available workflows[/bold]")
    for workflow in workflows:
        console.print()
        console.print(f"[bold cyan]{escape(workflow.id)}[/bold cyan] - {escape(workflow.display_name)}")
        console.print(f"  {escape(workflow.description)}")


def print_plan(plan: list[InstallPlanItem]) -> None:
    table = Table(title="Install plan")
    table.add_column("Kind")
    table.add_column("Target")
    table.add_column("Exists")
    table.add_column("Action")
    for item in plan:
        table.add_row(item.kind, str(item.target), "yes" if item.exists else "no", item.action.value if item.action else "")
    console.print(table)
