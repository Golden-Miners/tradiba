import uuid
from datetime import datetime
from tradiba.decision.simulator import DecisionSimulator
from tradiba.decision.models.decision import Decision, DecisionCategory, DecisionStatus

def test_decision_simulator():
    sim = DecisionSimulator()
    
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
    
    result = sim.simulate(d, {})
    assert result["projected_outcome"] == "positive"
