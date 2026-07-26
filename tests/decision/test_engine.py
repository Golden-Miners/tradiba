import uuid
from datetime import datetime
from tradiba.decision.models.decision import Decision, DecisionCategory, DecisionStatus
from tradiba.decision.engine import DecisionEngine

def test_decision_engine():
    engine = DecisionEngine()
    
    d1 = Decision(
        decision_id=uuid.uuid4(),
        category=DecisionCategory.DEPLOY_STRATEGY,
        created_at=datetime.utcnow(),
        status=DecisionStatus.PROPOSED,
        objective="test",
        confidence=0.95,
        evidence_ids=[],
        policy_results=[]
    )
    
    res1 = engine.process_decision(d1)
    assert res1.status == DecisionStatus.APPROVED
    
    d2 = Decision(
        decision_id=uuid.uuid4(),
        category=DecisionCategory.DEPLOY_STRATEGY,
        created_at=datetime.utcnow(),
        status=DecisionStatus.PROPOSED,
        objective="test",
        confidence=0.85,
        evidence_ids=[],
        policy_results=[]
    )
    
    res2 = engine.process_decision(d2)
    assert res2.status == DecisionStatus.PROPOSED
