from tradiba.hermes.core.governance import GovernanceEngine, HermesRecommendation

def test_governance_engine():
    engine = GovernanceEngine()
    rec = HermesRecommendation(id="rec1", description="Buy EURUSD", impact="High")
    
    # Submit recommendation
    engine.submit_recommendation(rec)
    assert len(engine.pending_approvals) == 1
    assert engine.pending_approvals[0].approved is False
    
    # Approve recommendation
    success = engine.approve("rec1")
    assert success is True
    assert len(engine.pending_approvals) == 0
    assert rec.approved is True
