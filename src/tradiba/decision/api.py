from fastapi import APIRouter
from uuid import UUID

router = APIRouter(prefix="/decisions", tags=["decisions"])

@router.get("/")
def list_decisions() -> dict:
    return {"status": "ok"}

@router.get("/{decision_id}")
def get_decision(decision_id: UUID) -> dict:
    return {"id": str(decision_id)}

@router.post("/{decision_id}/approve")
def approve_decision(decision_id: UUID) -> dict:
    return {"status": "approved"}

@router.post("/{decision_id}/reject")
def reject_decision(decision_id: UUID) -> dict:
    return {"status": "rejected"}
