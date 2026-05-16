from typer.testing import CliRunner

from qa_workflow_toolkit.cli import app


def test_list_outputs_workflows_without_table() -> None:
    result = CliRunner().invoke(app, ["list"])

    assert result.exit_code == 0
    assert "Available workflows" in result.output
    assert "test-design - テスト設計" not in result.output
    assert "scenario-test-design - シナリオテスト設計" in result.output
    assert "要件、業務フロー、画面仕様、ドメインルールからシナリオテストを設計する" in result.output
    assert "Agents:" not in result.output
    assert "┏" not in result.output
    assert "┃" not in result.output
