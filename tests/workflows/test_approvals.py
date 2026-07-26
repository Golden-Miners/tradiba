import uuid
from tradiba.workflows.approvals import ApprovalEngine, ApprovalRequest

def test_approval_engine():
    engine = ApprovalEngine()
    req_id = uuid.uuid4()
    req = ApprovalRequest(
        request_id=req_id,
        requester="alice",
        rationale="test",
        affected_resources=[],
        rollback_plan="none",
        policy="single_approver"
    )
    
    engine.request_approval(req)
    assert req.status == "pending"
    
    engine.grant_approval(req_id, "bob")
    assert req.status == "approved"
