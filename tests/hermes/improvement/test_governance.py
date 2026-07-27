"""Tests for Hermes Governance."""

from tradiba.hermes.improvement.governance.rules import PromotionGovernance
from tradiba.hermes.improvement.promotion.workflow import PromotionWorkflow

def test_governance_rules():
    gov = PromotionGovernance()
    assert gov.requires_human_approval() is True
    assert gov.validate_workflow("proposal_1") is True

def test_promotion_workflow():
    gov = PromotionGovernance()
    workflow = PromotionWorkflow(gov)
    
    # Will be false because human approval is required and we aren't mocking it here
    assert workflow.request_promotion("candidate_1", {}) is False
