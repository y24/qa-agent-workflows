from pathlib import Path
import json
import shutil
import uuid

import pytest
from typer.testing import CliRunner

from qa_workflow_toolkit.cli import app
from qa_workflow_toolkit.console import _gradient_color
from qa_workflow_toolkit.registry import get_workflow
from qa_workflow_toolkit.state import AGENTS_MD_KIND_WIKI, record_installed_workflows, record_repository_config


@pytest.fixture()
def workspace_tmp() -> Path:
    path = Path("work") / "test-tmp" / f"qatool-cli-test-{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


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


def test_no_args_opens_interactive_menu_and_can_show_help(monkeypatch: pytest.MonkeyPatch) -> None:
    prompts: list[str] = []
    choice_titles: list[list[str]] = []

    class FakeChoice:
        def __init__(self, title: str, value: str) -> None:
            self.title = title
            self.value = value

    class SelectPrompt:
        def __init__(self, message: str, choices: list[FakeChoice]) -> None:
            self.message = message
            self.choices = choices

        def ask(self) -> str:
            prompts.append(self.message)
            choice_titles.append([choice.title for choice in self.choices])
            return "help"

    class FakeQuestionary:
        Choice = FakeChoice

        @staticmethod
        def select(message: str, choices: list[FakeChoice], default: str | None = None) -> SelectPrompt:
            return SelectPrompt(message, choices)

    monkeypatch.setattr("qa_workflow_toolkit.cli._questionary", lambda: FakeQuestionary)

    result = CliRunner().invoke(app, [])

    assert result.exit_code == 0
    assert prompts == ["Select command"]
    assert choice_titles == [
        [
            "workflow - QA workflow skills のインストール、更新、削除",
            "wiki - LLM wiki の構築",
            "help - 利用できるコマンドと実行例を表示",
        ]
    ]
    assert "___      _       _____ ___" in result.output
    assert "Usage" in result.output


def test_interactive_workflow_list_hides_update_and_uninstall_without_installed_state(
    monkeypatch: pytest.MonkeyPatch,
    workspace_tmp: Path,
) -> None:
    workspace = workspace_tmp.resolve()
    monkeypatch.chdir(workspace)
    responses = ["workflow", "list"]
    prompts: list[str] = []
    choice_titles: list[list[str]] = []

    class FakeChoice:
        def __init__(self, title: str, value: str) -> None:
            self.title = title
            self.value = value

    class SelectPrompt:
        def __init__(self, message: str, choices: list[FakeChoice]) -> None:
            self.message = message
            self.choices = choices

        def ask(self) -> str:
            prompts.append(self.message)
            choice_titles.append([choice.title for choice in self.choices])
            return responses.pop(0)

    class FakeQuestionary:
        Choice = FakeChoice

        @staticmethod
        def select(message: str, choices: list[FakeChoice], default: str | None = None) -> SelectPrompt:
            return SelectPrompt(message, choices)

    monkeypatch.setattr("qa_workflow_toolkit.cli._questionary", lambda: FakeQuestionary)

    result = CliRunner().invoke(app, [])

    assert result.exit_code == 0
    assert prompts == ["Select command", "Select workflow operation"]
    assert choice_titles[1] == [
        "install - QA workflow skills をカレントディレクトリへ配置",
        "list - 利用可能な workflow 一覧を表示",
        "help - workflow コマンドのヘルプを表示",
    ]
    assert "Available workflows" in result.output
    assert "scenario-test-design - シナリオテスト設計" in result.output


def test_interactive_workflow_list_shows_update_and_uninstall_with_installed_state(
    monkeypatch: pytest.MonkeyPatch,
    workspace_tmp: Path,
) -> None:
    workspace = workspace_tmp.resolve()
    monkeypatch.chdir(workspace)
    record_installed_workflows(workspace, [get_workflow("scenario-test-design")], "roocode")
    responses = ["workflow", "list"]
    prompts: list[str] = []
    choice_titles: list[list[str]] = []

    class FakeChoice:
        def __init__(self, title: str, value: str) -> None:
            self.title = title
            self.value = value

    class SelectPrompt:
        def __init__(self, message: str, choices: list[FakeChoice]) -> None:
            self.message = message
            self.choices = choices

        def ask(self) -> str:
            prompts.append(self.message)
            choice_titles.append([choice.title for choice in self.choices])
            return responses.pop(0)

    class FakeQuestionary:
        Choice = FakeChoice

        @staticmethod
        def select(message: str, choices: list[FakeChoice], default: str | None = None) -> SelectPrompt:
            return SelectPrompt(message, choices)

    monkeypatch.setattr("qa_workflow_toolkit.cli._questionary", lambda: FakeQuestionary)

    result = CliRunner().invoke(app, [])

    assert result.exit_code == 0
    assert prompts == ["Select command", "Select workflow operation"]
    assert choice_titles[1] == [
        "install - QA workflow skills をカレントディレクトリへ配置",
        "update - インストール済みの workflow skills を最新版に更新",
        "uninstall - インストール済みの workflow skills を削除",
        "list - 利用可能な workflow 一覧を表示",
        "help - workflow コマンドのヘルプを表示",
    ]
    assert "Available workflows" in result.output
    assert "scenario-test-design - シナリオテスト設計" in result.output


def test_interactive_wiki_menu_hides_update_without_installed_state(
    monkeypatch: pytest.MonkeyPatch,
    workspace_tmp: Path,
) -> None:
    workspace = workspace_tmp.resolve()
    monkeypatch.chdir(workspace)
    responses = ["wiki", "help"]
    choice_titles: list[list[str]] = []

    class FakeChoice:
        def __init__(self, title: str, value: str) -> None:
            self.title = title
            self.value = value

    class SelectPrompt:
        def __init__(self, message: str, choices: list[FakeChoice]) -> None:
            self.choices = choices

        def ask(self) -> str:
            choice_titles.append([choice.title for choice in self.choices])
            return responses.pop(0)

    class FakeQuestionary:
        Choice = FakeChoice

        @staticmethod
        def select(message: str, choices: list[FakeChoice], default: str | None = None) -> SelectPrompt:
            return SelectPrompt(message, choices)

    monkeypatch.setattr("qa_workflow_toolkit.cli._questionary", lambda: FakeQuestionary)

    result = CliRunner().invoke(app, [])

    assert result.exit_code == 0
    assert choice_titles[1] == [
        "init - 現在のフォルダに LLM wiki assets を初期化",
        "help - wiki コマンドのヘルプを表示",
    ]


def test_interactive_wiki_menu_shows_update_with_installed_state(
    monkeypatch: pytest.MonkeyPatch,
    workspace_tmp: Path,
) -> None:
    workspace = workspace_tmp.resolve()
    monkeypatch.chdir(workspace)
    record_repository_config(workspace, "roocode", include_agents_md=False, agents_md_kind=AGENTS_MD_KIND_WIKI)
    responses = ["wiki", "help"]
    choice_titles: list[list[str]] = []

    class FakeChoice:
        def __init__(self, title: str, value: str) -> None:
            self.title = title
            self.value = value

    class SelectPrompt:
        def __init__(self, message: str, choices: list[FakeChoice]) -> None:
            self.choices = choices

        def ask(self) -> str:
            choice_titles.append([choice.title for choice in self.choices])
            return responses.pop(0)

    class FakeQuestionary:
        Choice = FakeChoice

        @staticmethod
        def select(message: str, choices: list[FakeChoice], default: str | None = None) -> SelectPrompt:
            return SelectPrompt(message, choices)

    monkeypatch.setattr("qa_workflow_toolkit.cli._questionary", lambda: FakeQuestionary)

    result = CliRunner().invoke(app, [])

    assert result.exit_code == 0
    assert choice_titles[1] == [
        "init - 現在のフォルダに LLM wiki assets を初期化",
        "update - 初期化済みの LLM wiki assets を最新版に更新",
        "help - wiki コマンドのヘルプを表示",
    ]


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
        assert "Installed 3 item(s)." in result.output
        assert "Usage:" in result.output
        assert "/risk-based-test-design <入力資料>" in result.output
        assert "RooCodeで" not in result.output
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_wiki_init_creates_llm_wiki_assets() -> None:
    target = Path("work") / "test-tmp" / f"qatool-wiki-test-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    try:
        result = CliRunner().invoke(
            app,
            [
                "wiki",
                "init",
                "--name",
                "Research Wiki",
                "--agent",
                "roocode",
                "--target",
                str(target),
                "--yes",
            ],
        )

        assert result.exit_code == 0
        assert "Created 20 item(s)." in result.output
        assert (target / "AGENTS.md").is_file()
        assert (target / ".gitignore").read_text(encoding="utf-8") == ".obsidian\n.qatool\n.temp\n"
        assert (target / "raw" / ".gitkeep").is_file()
        assert (target / "wiki" / ".gitkeep").is_file()
        assert (target / "wiki" / "articles" / ".gitkeep").is_file()
        assert (target / "wiki" / "concepts" / ".gitkeep").is_file()
        assert (target / "wiki" / "queries" / ".gitkeep").is_file()
        assert (target / ".temp" / ".gitkeep").is_file()
        assert (target / "index.md").is_file()
        assert (target / "log.md").is_file()
        assert (target / ".roo" / "commands" / "ingest.md").is_file()
        assert (target / ".roo" / "commands" / "query.md").is_file()
        assert (target / ".roo" / "commands" / "lint.md").is_file()
        assert (target / ".roo" / "commands" / "convert.md").is_file()
        assert not (target / ".agents" / "skills").exists()
        metadata = json.loads((target / ".qatool" / "metadata.json").read_text(encoding="utf-8"))
        assert metadata["agent"] == "roocode"
        assert metadata["include_agents_md"] is False
        assert metadata["agents_md_kind"] == "wiki"
        assert metadata["wiki_type"] == "basic"
        assert metadata["workflows"] == []
        assert "Research Wiki LLM Wiki" in (target / "AGENTS.md").read_text(encoding="utf-8")
        assert 'markitdown "<input>" -o "<output>"' in (
            target / ".roo" / "commands" / "convert.md"
        ).read_text(encoding="utf-8")
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_wiki_init_appends_missing_gitignore_entries() -> None:
    target = Path("work") / "test-tmp" / f"qatool-wiki-gitignore-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    (target / ".gitignore").write_text("dist/\n.qatool\n", encoding="utf-8")
    try:
        result = CliRunner().invoke(app, ["wiki", "init", "--target", str(target), "--yes"])

        assert result.exit_code == 0
        assert "Created 19 item(s)." in result.output
        assert "Updated .gitignore with 2 entry(s)." in result.output
        assert (target / ".gitignore").read_text(encoding="utf-8") == "dist/\n.qatool\n.obsidian\n.temp\n"
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_wiki_init_accepts_basic_type_explicitly() -> None:
    target = Path("work") / "test-tmp" / f"qatool-wiki-basic-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    try:
        result = CliRunner().invoke(
            app,
            [
                "wiki",
                "init",
                "--name",
                "Basic Wiki",
                "--type",
                "Basic",
                "--agent",
                "roocode",
                "--target",
                str(target),
                "--yes",
            ],
        )
        metadata = json.loads((target / ".qatool" / "metadata.json").read_text(encoding="utf-8"))

        assert result.exit_code == 0
        assert metadata["wiki_type"] == "basic"
        assert "Basic Wiki LLM Wiki" in (target / "AGENTS.md").read_text(encoding="utf-8")
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_wiki_init_rejects_unknown_type() -> None:
    target = Path("work") / "test-tmp" / f"qatool-wiki-unknown-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    try:
        result = CliRunner().invoke(
            app,
            [
                "wiki",
                "init",
                "--type",
                "unknown",
                "--target",
                str(target),
                "--yes",
            ],
        )

        assert result.exit_code != 0
        assert "unsupported wiki type: unknown" in result.output
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_interactive_wiki_init_prompts_for_wiki_type(
    monkeypatch: pytest.MonkeyPatch,
    workspace_tmp: Path,
) -> None:
    workspace = workspace_tmp.resolve()
    monkeypatch.chdir(workspace)
    select_responses = ["wiki", "init", "basic", "roocode"]
    select_messages: list[str] = []
    text_messages: list[str] = []

    class FakeChoice:
        def __init__(self, title: str, value: str) -> None:
            self.title = title
            self.value = value

    class SelectPrompt:
        def __init__(self, message: str) -> None:
            self.message = message

        def ask(self) -> str:
            select_messages.append(self.message)
            return select_responses.pop(0)

    class TextPrompt:
        def __init__(self, message: str) -> None:
            self.message = message

        def ask(self) -> str:
            text_messages.append(self.message)
            return "Interactive Wiki"

    class ConfirmPrompt:
        def ask(self) -> bool:
            return True

    class FakeQuestionary:
        Choice = FakeChoice

        @staticmethod
        def select(message: str, choices: list[FakeChoice] | list[str], default: str | None = None) -> SelectPrompt:
            return SelectPrompt(message)

        @staticmethod
        def text(message: str, default: str) -> TextPrompt:
            return TextPrompt(message)

        @staticmethod
        def confirm(message: str, default: bool = True) -> ConfirmPrompt:
            return ConfirmPrompt()

    monkeypatch.setattr("qa_workflow_toolkit.cli._questionary", lambda: FakeQuestionary)

    result = CliRunner().invoke(app, [])
    metadata = json.loads((workspace / ".qatool" / "metadata.json").read_text(encoding="utf-8"))

    assert result.exit_code == 0
    assert text_messages == ["Wiki name"]
    assert select_messages == ["Select command", "Select wiki operation", "Select wiki type", "Select target agent"]
    assert metadata["wiki_type"] == "basic"
    assert "<!-- wiki-type: basic -->" in (workspace / "AGENTS.md").read_text(encoding="utf-8")


def test_wiki_init_uses_target_folder_name_by_default_with_yes() -> None:
    target = Path("work") / "test-tmp" / f"qatool-wiki-default-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    try:
        result = CliRunner().invoke(app, ["wiki", "init", "--target", str(target), "--yes"])

        assert result.exit_code == 0
        assert f"# {target.name} LLM Wiki" in (target / "AGENTS.md").read_text(encoding="utf-8")
        assert "Select target agent" not in result.output
    finally:
        shutil.rmtree(target, ignore_errors=True)

def test_wiki_update_overwrites_generated_wiki_assets_only() -> None:
    target = Path("work") / "test-tmp" / f"qatool-wiki-update-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    try:
        init_result = CliRunner().invoke(
            app,
            [
                "wiki",
                "init",
                "--name",
                "Research Wiki",
                "--agent",
                "roocode",
                "--target",
                str(target),
                "--yes",
            ],
        )
        command_path = target / ".roo" / "commands" / "ingest.md"
        index_path = target / "index.md"
        log_path = target / "log.md"
        command_path.write_text("modified command", encoding="utf-8")
        index_path.write_text("user index", encoding="utf-8")
        log_path.write_text("user log", encoding="utf-8")

        update_result = CliRunner().invoke(app, ["wiki", "update", "--target", str(target), "--yes"])

        assert init_result.exit_code == 0
        assert update_result.exit_code == 0
        assert "Updated 1 item(s)." in update_result.output
        assert "modified command" not in command_path.read_text(encoding="utf-8")
        assert index_path.read_text(encoding="utf-8") == "user index"
        assert log_path.read_text(encoding="utf-8") == "user log"
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_wiki_update_reuses_recorded_claude_agent() -> None:
    target = Path("work") / "test-tmp" / f"qatool-wiki-update-claude-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    try:
        init_result = CliRunner().invoke(
            app,
            [
                "wiki",
                "init",
                "--name",
                "Claude Wiki",
                "--agent",
                "claude",
                "--target",
                str(target),
                "--yes",
            ],
        )
        command_path = target / ".claude" / "commands" / "query.md"
        command_path.write_text("modified command", encoding="utf-8")

        update_result = CliRunner().invoke(app, ["wiki", "update", "--target", str(target), "--yes"])

        assert init_result.exit_code == 0
        assert update_result.exit_code == 0
        assert "Updated 1 item(s)." in update_result.output
        assert "modified command" not in command_path.read_text(encoding="utf-8")
        assert not (target / ".roo" / "commands" / "query.md").exists()
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_wiki_update_reports_no_updates_for_matching_assets() -> None:
    target = Path("work") / "test-tmp" / f"qatool-wiki-update-none-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    try:
        init_result = CliRunner().invoke(app, ["wiki", "init", "--target", str(target), "--yes"])
        update_result = CliRunner().invoke(app, ["wiki", "update", "--target", str(target), "--yes"])

        assert init_result.exit_code == 0
        assert update_result.exit_code == 0
        assert "No updates available." in update_result.output
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_workflow_install_reuses_agent_recorded_by_wiki_init(monkeypatch: pytest.MonkeyPatch) -> None:
    target = Path("work") / "test-tmp" / f"qatool-wiki-agent-reuse-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    try:
        wiki_result = CliRunner().invoke(
            app,
            [
                "wiki",
                "init",
                "--name",
                "Reuse Wiki",
                "--agent",
                "roocode",
                "--target",
                str(target),
                "--yes",
            ],
        )

        def fail_questionary():
            raise AssertionError("questionary should not be called when wiki init recorded the agent")

        monkeypatch.setattr("qa_workflow_toolkit.cli._questionary", fail_questionary)

        install_result = CliRunner().invoke(
            app,
            [
                "workflow",
                "install",
                "--workflow",
                "scenario-test-design",
                "--target",
                str(target),
                "--yes",
            ],
        )

        metadata = json.loads((target / ".qatool" / "metadata.json").read_text(encoding="utf-8"))

        assert wiki_result.exit_code == 0
        assert install_result.exit_code == 0
        assert metadata["agent"] == "roocode"
        assert metadata["workflows"][0]["workflow_id"] == "scenario-test-design"
        assert "Select target agent" not in install_result.output
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_workflow_uninstall_keeps_wiki_agents_md_when_state_identifies_it_as_wiki() -> None:
    target = Path("work") / "test-tmp" / f"qatool-wiki-agents-uninstall-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    try:
        wiki_result = CliRunner().invoke(
            app,
            [
                "wiki",
                "init",
                "--name",
                "Shared Wiki",
                "--agent",
                "roocode",
                "--target",
                str(target),
                "--yes",
            ],
        )
        install_result = CliRunner().invoke(
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
        uninstall_result = CliRunner().invoke(
            app,
            [
                "workflow",
                "uninstall",
                "--workflow",
                "scenario-test-design",
                "--target",
                str(target),
                "--yes",
            ],
        )

        metadata = json.loads((target / ".qatool" / "metadata.json").read_text(encoding="utf-8"))

        assert wiki_result.exit_code == 0
        assert install_result.exit_code == 0
        assert uninstall_result.exit_code == 0
        assert "AGENTS.md" not in uninstall_result.output
        assert (target / "AGENTS.md").is_file()
        assert "Shared Wiki LLM Wiki" in (target / "AGENTS.md").read_text(encoding="utf-8")
        assert metadata["agents_md_kind"] == "wiki"
        assert metadata["workflows"] == []
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_wiki_init_prompts_before_overwriting_existing_agents_md(monkeypatch: pytest.MonkeyPatch) -> None:
    target = Path("work") / "test-tmp" / f"qatool-wiki-existing-agents-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    (target / "AGENTS.md").write_text("existing instructions", encoding="utf-8")
    confirm_messages: list[str] = []
    confirm_defaults: list[bool] = []

    class ConfirmPrompt:
        def __init__(self, message: str) -> None:
            self.message = message

        def ask(self) -> bool:
            confirm_messages.append(self.message)
            return True

    class FakeQuestionary:
        @staticmethod
        def confirm(message: str, default: bool = True) -> ConfirmPrompt:
            confirm_defaults.append(default)
            return ConfirmPrompt(message)

    try:
        monkeypatch.setattr("qa_workflow_toolkit.cli._questionary", lambda: FakeQuestionary)

        result = CliRunner().invoke(
            app,
            [
                "wiki",
                "init",
                "--name",
                "Existing Wiki",
                "--agent",
                "roocode",
                "--target",
                str(target),
            ],
        )

        assert result.exit_code == 0
        assert confirm_messages == [
            f"{target.resolve()}\\AGENTS.md already exists. Overwrite it with LLM wiki AGENTS.md?",
            "Initialize this LLM wiki?",
        ]
        assert confirm_defaults == [True, True]
        assert "Overwritten 1 item(s)." in result.output
        assert "Existing Wiki LLM Wiki" in (target / "AGENTS.md").read_text(encoding="utf-8")
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_install_does_not_create_agents_md() -> None:
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
        assert "Installed 3 item(s)." in result.output
        assert not (target / "AGENTS.md").exists()
        assert (target / ".agents" / "shared" / "common_contract.md").is_file()
        assert (target / ".agents" / "skills" / "risk-based-test-design" / "SKILL.md").is_file()
        assert (target / ".roo" / "commands" / "risk-based-test-design.md").is_file()
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_install_creates_copilot_prompt_file() -> None:
    target = Path("work") / "test-tmp" / f"qatool-cli-copilot-{uuid.uuid4().hex}"
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
                "copilot",
                "--target",
                str(target),
                "--yes",
            ],
        )

        assert result.exit_code == 0
        assert (target / ".github" / "prompts" / "risk-based-test-design.prompt.md").is_file()
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_install_creates_codex_prompt_file() -> None:
    target = Path("work") / "test-tmp" / f"qatool-cli-codex-{uuid.uuid4().hex}"
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
                "codex",
                "--target",
                str(target),
                "--yes",
            ],
        )

        assert result.exit_code == 0
        assert (target / ".codex" / "prompts" / "risk-based-test-design.md").is_file()
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_install_records_workflow_metadata() -> None:
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
        metadata = json.loads((target / ".qatool" / "metadata.json").read_text(encoding="utf-8"))

        assert result.exit_code == 0
        assert metadata["schema_version"] == 1
        assert metadata["agent"] == "roocode"
        assert metadata["include_agents_md"] is False
        assert metadata["workflows"][0]["workflow_id"] == "risk-based-test-design"
        assert "agent" not in metadata["workflows"][0]
        assert "include_agents_md" not in metadata["workflows"][0]
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_install_reuses_recorded_agent(monkeypatch: pytest.MonkeyPatch) -> None:
    target = Path("work") / "test-tmp" / f"qatool-cli-test-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    try:
        first_result = CliRunner().invoke(
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

        def fail_questionary():
            raise AssertionError("questionary should not be called when install metadata has reusable defaults")

        monkeypatch.setattr("qa_workflow_toolkit.cli._questionary", fail_questionary)

        second_result = CliRunner().invoke(
            app,
            [
                "workflow",
                "install",
                "--workflow",
                "scenario-test-design",
                "--target",
                str(target),
                "--yes",
            ],
        )
        metadata = json.loads((target / ".qatool" / "metadata.json").read_text(encoding="utf-8"))
        installed = {item["workflow_id"]: item for item in metadata["workflows"]}

        assert first_result.exit_code == 0
        assert second_result.exit_code == 0
        assert not (target / "AGENTS.md").exists()
        assert metadata["agent"] == "roocode"
        assert metadata["include_agents_md"] is False
        assert "agent" not in installed["scenario-test-design"]
        assert "include_agents_md" not in installed["scenario-test-design"]
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
        assert "Skipped 3 item(s)." in second_result.output
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_update_overwrites_installed_assets() -> None:
    target = Path("work") / "test-tmp" / f"qatool-cli-test-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    try:
        install_result = CliRunner().invoke(
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
        command_path = target / ".roo" / "commands" / "scenario-test-design.md"
        command_path.write_text("modified", encoding="utf-8")
        update_result = CliRunner().invoke(
            app,
            [
                "workflow",
                "update",
                "--workflow",
                "scenario-test-design",
                "--target",
                str(target),
                "--yes",
            ],
        )

        assert install_result.exit_code == 0
        assert update_result.exit_code == 0
        assert "Updated 1 item(s)." in update_result.output
        assert "no change" not in update_result.output
        assert "Select target agent" not in update_result.output
        assert "modified" not in command_path.read_text(encoding="utf-8")
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_update_asks_once_without_per_file_collision_prompts(monkeypatch: pytest.MonkeyPatch) -> None:
    target = Path("work") / "test-tmp" / f"qatool-cli-test-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    prompts: list[str] = []

    class ConfirmPrompt:
        def __init__(self, message: str) -> None:
            self.message = message

        def ask(self) -> bool:
            prompts.append(self.message)
            return True

    class FakeQuestionary:
        @staticmethod
        def confirm(message: str, default: bool = True) -> ConfirmPrompt:
            return ConfirmPrompt(message)

    try:
        install_result = CliRunner().invoke(
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
        command_path = target / ".roo" / "commands" / "scenario-test-design.md"
        command_path.write_text("modified", encoding="utf-8")
        monkeypatch.setattr("qa_workflow_toolkit.cli._questionary", lambda: FakeQuestionary)

        update_result = CliRunner().invoke(
            app,
            [
                "workflow",
                "update",
                "--workflow",
                "scenario-test-design",
                "--target",
                str(target),
            ],
        )

        assert install_result.exit_code == 0
        assert update_result.exit_code == 0
        assert prompts == ["Update these files?"]
        assert "Updated 1 item(s)." in update_result.output
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_uninstall_removes_workflow_specific_assets() -> None:
    target = Path("work") / "test-tmp" / f"qatool-cli-test-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    try:
        install_result = CliRunner().invoke(
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
        uninstall_result = CliRunner().invoke(
            app,
            [
                "workflow",
                "uninstall",
                "--workflow",
                "scenario-test-design",
                "--agent",
                "roocode",
                "--target",
                str(target),
                "--yes",
            ],
        )

        assert install_result.exit_code == 0
        assert uninstall_result.exit_code == 0
        assert "Removed 3 item(s)." in uninstall_result.output
        assert not (target / ".agents" / "skills" / "scenario-test-design").exists()
        assert not (target / ".roo" / "commands" / "scenario-test-design.md").exists()
        assert not (target / ".agents" / "shared").exists()
        assert not (target / ".qatool" / "metadata.json").exists()
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_uninstall_without_workflow_prompts_for_installed_workflows_only(monkeypatch: pytest.MonkeyPatch) -> None:
    target = Path("work") / "test-tmp" / f"qatool-cli-test-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    select_messages: list[str] = []
    select_choices: list[list[tuple[str, str]]] = []

    class FakeChoice:
        def __init__(self, title: str, value: str) -> None:
            self.title = title
            self.value = value

    class SelectPrompt:
        def __init__(self, message: str, choices: list[FakeChoice]) -> None:
            self.message = message
            self.choices = choices

        def ask(self) -> str:
            select_messages.append(self.message)
            select_choices.append([(choice.title, choice.value) for choice in self.choices])
            return "risk-based-test-design"

    class FakeQuestionary:
        Choice = FakeChoice

        @staticmethod
        def select(message: str, choices: list[FakeChoice], default: str | None = None) -> SelectPrompt:
            return SelectPrompt(message, choices)

    try:
        first_install = CliRunner().invoke(
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
        second_install = CliRunner().invoke(
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
        monkeypatch.setattr("qa_workflow_toolkit.cli._questionary", lambda: FakeQuestionary)

        uninstall_result = CliRunner().invoke(
            app,
            [
                "workflow",
                "uninstall",
                "--target",
                str(target),
                "--yes",
            ],
        )

        assert first_install.exit_code == 0
        assert second_install.exit_code == 0
        assert uninstall_result.exit_code == 0
        assert select_messages == ["Select workflow to uninstall"]
        assert select_choices == [
            [
                ("all - インストール済みのすべてのworkflow", "all"),
                ("scenario-test-design - シナリオテスト設計", "scenario-test-design"),
                ("risk-based-test-design - リスクベーステスト設計", "risk-based-test-design"),
            ]
        ]
        assert "Removed 2 item(s)." in uninstall_result.output
        assert (target / ".agents" / "skills" / "scenario-test-design" / "SKILL.md").is_file()
        assert not (target / ".agents" / "skills" / "risk-based-test-design").exists()
        assert not (target / ".roo" / "commands" / "risk-based-test-design.md").exists()
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_uninstall_keeps_common_assets_when_other_workflows_remain() -> None:
    target = Path("work") / "test-tmp" / f"qatool-cli-test-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    try:
        first_install = CliRunner().invoke(
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
        second_install = CliRunner().invoke(
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
        uninstall_result = CliRunner().invoke(
            app,
            [
                "workflow",
                "uninstall",
                "--workflow",
                "risk-based-test-design",
                "--target",
                str(target),
                "--yes",
            ],
        )

        assert first_install.exit_code == 0
        assert second_install.exit_code == 0
        assert uninstall_result.exit_code == 0
        assert "Removed 2 item(s)." in uninstall_result.output
        assert not (target / "AGENTS.md").exists()
        assert (target / ".agents" / "shared" / "common_contract.md").is_file()
        assert (target / ".qatool" / "metadata.json").is_file()
        assert (target / ".agents" / "skills" / "scenario-test-design" / "SKILL.md").is_file()
        assert not (target / ".agents" / "skills" / "risk-based-test-design").exists()
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_uninstall_confirm_defaults_to_yes(monkeypatch: pytest.MonkeyPatch) -> None:
    target = Path("work") / "test-tmp" / f"qatool-cli-test-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    confirm_defaults: list[bool] = []

    class ConfirmPrompt:
        def ask(self) -> bool:
            return True

    class FakeQuestionary:
        @staticmethod
        def confirm(message: str, default: bool = True) -> ConfirmPrompt:
            confirm_defaults.append(default)
            return ConfirmPrompt()

    try:
        install_result = CliRunner().invoke(
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
        monkeypatch.setattr("qa_workflow_toolkit.cli._questionary", lambda: FakeQuestionary)

        uninstall_result = CliRunner().invoke(
            app,
            [
                "workflow",
                "uninstall",
                "--workflow",
                "scenario-test-design",
                "--target",
                str(target),
            ],
        )

        assert install_result.exit_code == 0
        assert uninstall_result.exit_code == 0
        assert confirm_defaults == [True]
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_uninstall_plan_hides_missing_targets() -> None:
    target = Path("work") / "test-tmp" / f"qatool-cli-test-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    try:
        install_result = CliRunner().invoke(
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
        uninstall_result = CliRunner().invoke(
            app,
            [
                "workflow",
                "uninstall",
                "--workflow",
                "all",
                "--target",
                str(target),
                "--yes",
            ],
        )

        assert install_result.exit_code == 0
        assert uninstall_result.exit_code == 0
        assert "AGENTS.md" not in uninstall_result.output
        assert "│ agents_md " not in uninstall_result.output
        assert "Removed 3 item(s)." in uninstall_result.output
        assert "Skipped" not in uninstall_result.output
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_uninstall_plan_does_not_manage_existing_agents_md() -> None:
    target = Path("work") / "test-tmp" / f"qatool-cli-test-{uuid.uuid4().hex}"
    target.mkdir(parents=True)
    try:
        install_result = CliRunner().invoke(
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
        (target / "AGENTS.md").write_text("project specific instructions", encoding="utf-8")
        uninstall_result = CliRunner().invoke(
            app,
            [
                "workflow",
                "uninstall",
                "--workflow",
                "all",
                "--target",
                str(target),
                "--yes",
            ],
        )

        assert install_result.exit_code == 0
        assert uninstall_result.exit_code == 0
        assert "AGENTS.md" not in uninstall_result.output
        assert "│ agents_md " not in uninstall_result.output
        assert "Removed 3 item(s)." in uninstall_result.output
        assert "Skipped" not in uninstall_result.output
        assert (target / "AGENTS.md").read_text(encoding="utf-8") == "project specific instructions"
    finally:
        shutil.rmtree(target, ignore_errors=True)

