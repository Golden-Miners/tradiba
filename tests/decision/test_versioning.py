import uuid
from datetime import datetime
from tradiba.decision.versioning import DecisionVersioning
from tradiba.decision.repository import DecisionRepository
from tradiba.decision.models.decision import Decision, DecisionCategory, DecisionStatus

def test_decision_versioning():
    repo = DecisionRepository()
    versioning = DecisionVersioning(repo)
    
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
    
    versioning.commit_revision(d)
    
    retrieved = repo.get_latest(d.decision_id)
    assert retrieved is not None
    assert retrieved.status == DecisionStatus.PROPOSED
