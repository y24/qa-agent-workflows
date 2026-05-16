from pathlib import Path
import shutil
import uuid

import pytest
from typer.testing import CliRunner

from qa_workflow_toolkit.cli import _resolve_agents_md_choice, app
from qa_workflow_toolkit.console import _gradient_color
from qa_workflow_toolkit.installer import apply_default_actions, build_install_plan, install_from_plan
from qa_workflow_toolkit.models import CollisionAction
from qa_workflow_toolkit.registry import get_workflow


def test_header_gradient_uses_logo_colors() -> None:
    assert _gradient_color(0) == "#ff0d4f"
    assert _gradient_color(1) == "#f2a073"


def test_list_outputs_workflows_without_table() -> None:
    result = CliRunner().invoke(app, ["workflow", "list"])

    assert result.exit_code == 0
    assert "___      _       _____ ___" in result.output
    assert "Available workflows" in result.output
    assert "test-design - テスト設計" not in result.output
    assert "scenario-test-design - シナリオテスト設計" in result.output
    assert "要件、業務フロー、画面仕様、ドメインルールからシナリオテストを設計する" in result.output
    assert "Agents:" not in result.output
    assert "┏" not in result.output
    assert "┃" not in result.output


def test_install_outputs_example_prompt() -> None:
    target = Path("work") / "test-tmp" / f"qatool-cli-test-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    try:
        result = CliRunner().invoke(
            app,
            [
                "workflow",
                "install",
                "--workflow",
                "risk-based-test-design",
                "--agent",
                "roocode",
                "--target",
                str(target),
                "--yes",
            ],
        )

        assert result.exit_code == 0
        assert "create" in result.output
        assert "overwrite" not in result.output
        assert "Installed 4 item(s)." in result.output
        assert "Usage:" in result.output
        assert "/risk-based-test-design <入力資料>" in result.output
        assert "RooCodeで" not in result.output
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_install_can_skip_agents_md() -> None:
    target = Path("work") / "test-tmp" / f"qatool-cli-test-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    try:
        result = CliRunner().invoke(
            app,
            [
                "workflow",
                "install",
                "--workflow",
                "risk-based-test-design",
                "--agent",
                "roocode",
                "--target",
                str(target),
                "--no-agents-md",
                "--yes",
            ],
        )

        assert result.exit_code == 0
        assert "Installed 3 item(s)." in result.output
        assert not (target / "AGENTS.md").exists()
        assert (target / ".agents" / "shared" / "common_contract.md").is_file()
        assert (target / ".agents" / "skills" / "risk-based-test-design" / "SKILL.md").is_file()
        assert (target / ".roo" / "commands" / "risk-based-test-design.md").is_file()
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_install_outputs_no_change_for_matching_existing_assets() -> None:
    target = Path("work") / "test-tmp" / f"qatool-cli-test-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    try:
        first_result = CliRunner().invoke(
            app,
            [
                "workflow",
                "install",
                "--workflow",
                "scenario-test-design",
                "--agent",
                "roocode",
                "--target",
                str(target),
                "--yes",
            ],
        )
        second_result = CliRunner().invoke(
            app,
            [
                "workflow",
                "install",
                "--workflow",
                "scenario-test-design",
                "--agent",
                "roocode",
                "--target",
                str(target),
                "--yes",
            ],
        )

        assert first_result.exit_code == 0
        assert second_result.exit_code == 0
        assert "no change" in second_result.output
        assert "Installed 0 item(s)." in second_result.output
        assert "Skipped 4 item(s)." in second_result.output
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_agents_md_choice_skips_prompt_when_existing_file_matches(monkeypatch: pytest.MonkeyPatch) -> None:
    target = Path("work") / "test-tmp" / f"qatool-cli-test-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    try:
        workflow = get_workflow("scenario-test-design")
        plan = apply_default_actions(build_install_plan(workflow, target, "roocode"), CollisionAction.OVERWRITE)
        install_from_plan(plan)

        def fail_questionary():
            raise AssertionError("questionary should not be called for matching AGENTS.md")

        monkeypatch.setattr("qa_workflow_toolkit.cli._questionary", fail_questionary)

        assert _resolve_agents_md_choice(None, False, target, "roocode") is True
    finally:
        shutil.rmtree(target, ignore_errors=True)
