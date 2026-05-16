from typer.testing import CliRunner

from qa_workflow_toolkit.cli import app


def test_list_outputs_workflows_without_table() -> None:
    result = CliRunner().invoke(app, ["list"])

    assert result.exit_code == 0
    assert "Available workflows" in result.output
    assert "test-design - テスト設計" in result.output
    assert "入力資料から適切なQA workflowを選び" in result.output
    assert "段階的にテスト設計を開始する総合入口" in result.output
    assert "Agents:" not in result.output
    assert "┏" not in result.output
    assert "┃" not in result.output
