import uuid
from datetime import datetime
from tradiba.decision.explain import ExplainabilityEngine
from tradiba.decision.models.decision import Decision, DecisionCategory, DecisionStatus

def test_explainability_engine():
    engine = ExplainabilityEngine()
    
    d = Decision(
        decision_id=uuid.uuid4(),
        category=DecisionCategory.DEPLOY_STRATEGY,
        created_at=datetime.utcnow(),
        status=DecisionStatus.PROPOSED,
        objective="test",
        confidence=0.95,
        evidence_ids=[],
        policy_results=[]
    )
    
    exp = engine.explain(d)
    assert "DEPLOY_STRATEGY" in exp.decision_summary
    assert exp.confidence == 0.95
