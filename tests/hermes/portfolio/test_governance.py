from tradiba.hermes.portfolio.governance.workflow import GovernanceWorkflow

def test_governance_blocks_live():
    workflow = GovernanceWorkflow({"environment": "live"})
    # Even if risk approved, live execution should be blocked autonomously
    assert not workflow.approve_proposal({}, risk_approved=True)
    assert workflow.block_live_execution()

def test_governance_allows_digital_twin():
    workflow = GovernanceWorkflow({"environment": "digital_twin"})
    assert workflow.approve_proposal({}, risk_approved=True)
    assert not workflow.approve_proposal({}, risk_approved=False)
    assert not workflow.block_live_execution()
