from __future__ import annotations

from importlib import resources

from rich.console import Console
from rich.markup import escape
from rich.table import Table
from rich.text import Text

from .models import InstallPlanItem, UninstallPlanItem, WorkflowManifest
from .wiki import WikiInitItem

console = Console()


def print_header() -> None:
    console.print(_gradient_logo())
    console.print("CLI installer for QA agent workflow assets.\n")


def _gradient_logo() -> Text:
    logo = resources.files("qa_workflow_toolkit").joinpath("assets/logo.txt").read_text(encoding="utf-8").rstrip("\n")
    lines = logo.splitlines()
    width = max(len(line) for line in lines)
    text = Text()
    for line_index, line in enumerate(lines):
        for column_index, char in enumerate(line):
            ratio = column_index / max(width - 1, 1)
            text.append(char, style=f"bold {_gradient_color(ratio)}" if char != " " else None)
        if line_index < len(lines) - 1:
            text.append("\n")
    return text


def _gradient_color(ratio: float) -> str:
    start = (255, 13, 79)
    end = (242, 160, 115)
    red = round(start[0] + (end[0] - start[0]) * ratio)
    green = round(start[1] + (end[1] - start[1]) * ratio)
    blue = round(start[2] + (end[2] - start[2]) * ratio)
    return f"#{red:02x}{green:02x}{blue:02x}"


def print_usage() -> None:
    print_header()
    console.print("[bold]Usage[/bold]")
    console.print("  qatool wiki init           Initialize an LLM wiki in current folder")
    console.print("  qatool workflow install    Install QA workflow assets into current folder")
    console.print("  qatool workflow update     Update installed QA workflow assets")
    console.print("  qatool workflow uninstall  Remove installed QA workflow assets")
    console.print("  qatool workflow list       Show available workflows\n")
    console.print("[bold]Examples[/bold]")
    console.print("  qatool wiki init")
    console.print("  qatool wiki init --name research-notes --agent roocode --yes")
    console.print("  qatool wiki init --name research-notes --agent claude --yes")
    console.print("  qatool workflow install")
    console.print("  qatool workflow install --workflow scenario-test-design --agent roocode --yes")
    console.print("  qatool workflow install --workflow scenario-test-design --agent claude --yes")
    console.print("  qatool workflow install --workflow all --agent roocode --yes")
    console.print("  qatool workflow update --workflow all --agent roocode --yes")
    console.print("  qatool workflow uninstall --workflow scenario-test-design --agent roocode --yes")


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
        table.add_row(item.kind, str(item.target), "yes" if item.exists else "no", _plan_action_label(item))
    console.print(table)


def print_uninstall_plan(plan: list[UninstallPlanItem]) -> None:
    table = Table(title="Uninstall plan")
    table.add_column("Kind")
    table.add_column("Target")
    table.add_column("Exists")
    table.add_column("Action")
    for item in plan:
        if not item.exists:
            continue
        table.add_row(
            item.kind,
            str(item.target),
            "yes" if item.exists else "no",
            "remove" if item.safe_to_remove else "skip",
        )
    console.print(table)


def print_wiki_init_plan(plan: list[WikiInitItem], overwrite: bool, overwrite_targets: set | None = None) -> None:
    overwrite_targets = overwrite_targets or set()
    table = Table(title="Wiki init plan")
    table.add_column("Kind")
    table.add_column("Target")
    table.add_column("Exists")
    table.add_column("Action")
    for item in plan:
        table.add_row(
            item.kind,
            str(item.target),
            "yes" if item.exists else "no",
            _wiki_init_action_label(item, overwrite, overwrite_targets),
        )
    console.print(table)


def _plan_action_label(item: InstallPlanItem) -> str:
    if not item.exists:
        return "create"
    return item.action.value if item.action else ""


def _wiki_init_action_label(item: WikiInitItem, overwrite: bool, overwrite_targets: set) -> str:
    if not item.exists:
        return "create"
    if item.is_dir:
        return "keep"
    return "overwrite" if overwrite or item.target in overwrite_targets else "skip"
