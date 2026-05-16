from qa_workflow_toolkit.registry import get_workflow, load_workflows


def test_load_workflows_contains_test_design() -> None:
    workflows = load_workflows()
    workflow_ids = {workflow.id for workflow in workflows}

    assert "test-design" in workflow_ids
    assert "scenario-test-design" in workflow_ids
    assert "defect-analysis" in workflow_ids


def test_manifest_contains_install_targets() -> None:
    workflow = get_workflow("test-design")

    assert workflow.default_agent == "roocode"
    assert workflow.install.shared.target == ".agents/shared"
    assert workflow.install.skill.target == ".agents/skills/test-design"
    assert workflow.install.command.target == ".roo/commands/test-design.md"
