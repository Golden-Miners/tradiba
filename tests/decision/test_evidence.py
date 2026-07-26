import uuid
from datetime import datetime
from tradiba.decision.evidence import EvidenceEngine
from tradiba.decision.models.evidence import Evidence

def test_evidence_engine():
    engine = EvidenceEngine()
    
    eid = uuid.uuid4()
    e = Evidence(
        evidence_id=eid,
        source="test",
        created_at=datetime.utcnow(),
        content="some evidence"
    )
    
    engine.register(e)
    
    retrieved = engine.get_evidence(eid)
    assert retrieved is not None
    assert retrieved.content == "some evidence"
