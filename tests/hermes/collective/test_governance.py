import pytest
from unittest.mock import Mock
from tradiba.hermes.collective.governance.collective_governance import CollectiveGovernance
from tradiba.hermes.collective.consensus.engine import ConsensusEngine

def test_collective_governance_rejects_failed_consensus():
    # Mocking isn't strictly necessary if we pass dummy objects, but we'll test the logic
    engine = ConsensusEngine()
    mock_approval = Mock()
    mock_approval.process_decision.return_value = "APPROVED"
    
    gov = CollectiveGovernance(engine, mock_approval)
    
    rec = {"consensus_status": "REJECTED"}
    result = gov.process_collective_recommendation(rec, {})
    
    assert result == "REJECTED_BY_CONSENSUS"
    mock_approval.process_decision.assert_not_called()

def test_collective_governance_passes_approved_consensus():
    engine = ConsensusEngine()
    mock_approval = Mock()
    mock_approval.process_decision.return_value = "PENDING_HUMAN"
    
    gov = CollectiveGovernance(engine, mock_approval)
    
    rec = {
        "consensus_status": "APPROVED",
        "decision": {"symbol": "BTC"},
        "risk_approved": True
    }
    result = gov.process_collective_recommendation(rec, {})
    
    assert result == "PENDING_HUMAN"
    mock_approval.process_decision.assert_called_once_with({"symbol": "BTC"}, {}, True)
