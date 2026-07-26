from dataclasses import dataclass, field
import uuid

@dataclass
class ApprovalRequest:
    request_id: uuid.UUID
    requester: str
    rationale: str
    affected_resources: list[str]
    rollback_plan: str
    policy: str # e.g. 'single_approver', 'two_person'
    status: str = "pending"
    approvals: list[str] = field(default_factory=list) # List of approver IDs

class ApprovalEngine:
    """Evaluates approval policies."""
    
    def __init__(self) -> None:
        self._requests: dict[uuid.UUID, ApprovalRequest] = {}
        
    def request_approval(self, request: ApprovalRequest) -> None:
        self._requests[request.request_id] = request
        
    def grant_approval(self, request_id: uuid.UUID, approver_id: str) -> None:
        request = self._requests.get(request_id)
        if not request:
            raise ValueError(f"Request {request_id} not found.")
            
        if approver_id not in request.approvals:
            request.approvals.append(approver_id)
            
        self._evaluate_policy(request)

    def _evaluate_policy(self, request: ApprovalRequest) -> None:
        if request.policy == "single_approver":
            if len(request.approvals) >= 1:
                request.status = "approved"
        elif request.policy == "two_person":
            if len(request.approvals) >= 2:
                request.status = "approved"
