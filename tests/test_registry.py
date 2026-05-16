from qa_workflow_toolkit.registry import get_workflow, load_workflows


def test_load_workflows_contains_expected_workflows() -> None:
    workflows = load_workflows()
    workflow_ids = {workflow.id for workflow in workflows}

    assert "test-design" not in workflow_ids
    assert "scenario-test-design" in workflow_ids
    assert "defect-analysis" in workflow_ids


def test_manifest_contains_install_targets() -> None:
    workflow = get_workflow("scenario-test-design")

    assert workflow.default_agent == "roocode"
    assert workflow.install.shared.target == ".agents/shared"
    assert workflow.install.skill.target == ".agents/skills/scenario-test-design"
    assert workflow.install.command.target == ".roo/commands/scenario-test-design.md"
