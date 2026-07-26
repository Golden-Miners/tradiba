import uuid
from datetime import datetime
from tradiba.decision.policy import PolicyEngine
from tradiba.decision.models.decision import Decision, DecisionCategory, DecisionStatus

def test_policy_engine():
    engine = PolicyEngine()
    
    d = Decision(
        decision_id=uuid.uuid4(),
        category=DecisionCategory.DEPLOY_STRATEGY,
        created_at=datetime.utcnow(),
        status=DecisionStatus.PROPOSED,
        objective="test",
        confidence=0.9,
        evidence_ids=[],
        policy_results=[]
    )
    
    results = engine.evaluate(d)
    assert len(results) == 1
    assert results[0].result is True
