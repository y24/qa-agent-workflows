from pathlib import Path
import shutil
import uuid

from typer.testing import CliRunner

from qa_workflow_toolkit.cli import app
from qa_workflow_toolkit.console import _gradient_color


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
