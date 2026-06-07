from qa_workflow_toolkit.models import WikiTypeManifest, WorkflowManifest
from qa_workflow_toolkit.registry import (
    _wiki_type_sort_key,
    _workflow_sort_key,
    default_wiki_type,
    get_wiki_type,
    get_workflow,
    load_wiki_types,
    load_workflows,
)


def test_load_workflows_contains_expected_workflows() -> None:
    workflows = load_workflows()
    workflow_ids = {workflow.id for workflow in workflows}

    assert "test-design" not in workflow_ids
    assert "scenario-test-design" in workflow_ids
    assert "defect-analysis" in workflow_ids


def test_load_workflows_uses_manifest_sort_order() -> None:
    workflows = load_workflows()

    assert [workflow.id for workflow in workflows] == [
        "scenario-test-design",
        "risk-based-test-design",
        "spec-extraction",
        "testcase-viewpoint-extraction",
        "defect-analysis",
        "test-design-review",
        "nonfunctional-quality-criteria-planning",
        "system-test-strategy-planning",
        "pr-change-analysis",
    ]


def test_manifest_contains_install_targets() -> None:
    workflow = get_workflow("scenario-test-design")

    assert workflow.sort_order == 100
    assert workflow.default_agent == "roocode"
    assert workflow.supported_agents == ("roocode", "claude", "copilot", "codex")
    assert workflow.install.shared.target == ".agents/shared"
    assert workflow.install.skill.target == ".agents/skills/scenario-test-design"
    assert workflow.install.command.source == "commands/scenario-test-design.md"


def test_workflows_without_sort_order_sort_after_ordered_workflows_by_id() -> None:
    ordered = _workflow_from_dict("ordered-workflow", sort_order=100)
    unordered_b = _workflow_from_dict("zeta-workflow")
    unordered_a = _workflow_from_dict("alpha-workflow")

    workflows = sorted([unordered_b, ordered, unordered_a], key=_workflow_sort_key)

    assert [workflow.id for workflow in workflows] == [
        "ordered-workflow",
        "alpha-workflow",
        "zeta-workflow",
    ]
    assert unordered_a.sort_order is None


def test_load_wiki_types_reads_asset_manifests() -> None:
    wiki_types = load_wiki_types()

    assert [wiki_type.id for wiki_type in wiki_types] == ["basic", "test-viewpoint", "defect-knowledge"]
    assert wiki_types[0].display_name == "Basic Wiki"
    assert wiki_types[0].description == "汎用的なLLM wikiを構築"
    assert wiki_types[1].display_name == "Test Viewpoint Wiki"
    assert wiki_types[2].display_name == "Defect Knowledge Wiki"


def test_default_wiki_type_uses_manifest_default_flag() -> None:
    wiki_type = default_wiki_type()

    assert wiki_type.id == "basic"
    assert wiki_type.is_default is True


def test_get_wiki_type_accepts_id_and_display_name() -> None:
    assert get_wiki_type("basic").id == "basic"
    assert get_wiki_type("Basic").id == "basic"


def test_wiki_types_without_sort_order_sort_after_ordered_types_by_id() -> None:
    ordered = _wiki_type_from_dict("ordered", sort_order=100)
    unordered_b = _wiki_type_from_dict("zeta")
    unordered_a = _wiki_type_from_dict("alpha")

    wiki_types = sorted([unordered_b, ordered, unordered_a], key=_wiki_type_sort_key)

    assert [wiki_type.id for wiki_type in wiki_types] == [
        "ordered",
        "alpha",
        "zeta",
    ]


def _workflow_from_dict(workflow_id: str, sort_order: int | None = None) -> WorkflowManifest:
    data = {
        "id": workflow_id,
        "display_name": workflow_id,
        "description": workflow_id,
        "version": "0.1.0",
        "skill_name": workflow_id,
        "command_name": workflow_id,
        "default_agent": "roocode",
        "install": {
            "shared": {"source": "shared", "target": ".agents/shared"},
            "skill": {"source": f"workflows/{workflow_id}/skill", "target": f".agents/skills/{workflow_id}"},
            "command": {"source": f"commands/{workflow_id}.md", "target": f".roo/commands/{workflow_id}.md"},
        },
        "post_install_message": f"/{workflow_id} <入力資料>",
    }
    if sort_order is not None:
        data["sort_order"] = sort_order
    return WorkflowManifest.from_dict(data)


def _wiki_type_from_dict(wiki_type_id: str, sort_order: int | None = None) -> WikiTypeManifest:
    data = {
        "id": wiki_type_id,
        "display_name": wiki_type_id,
        "description": wiki_type_id,
        "version": "1.0.0",
    }
    if sort_order is not None:
        data["sort_order"] = sort_order
    return WikiTypeManifest.from_dict(data)
