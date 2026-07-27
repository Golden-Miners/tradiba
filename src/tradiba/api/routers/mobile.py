from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any

# Mock dependency for user retrieval (this would be injected in reality)
def get_current_user():
    return {"id": "u1", "roles": ["trader"]}

router = APIRouter(prefix="/mobile", tags=["Mobile Companion"])

@router.get("/dashboard")
async def get_mobile_dashboard(user: dict = Depends(get_current_user)):
    """Returns a summarized dashboard optimized for mobile view."""
    return {
        "status": "active",
        "alerts_count": 3,
        "portfolio_value": 1250000.0
    }

@router.get("/notifications")
async def get_mobile_notifications(user: dict = Depends(get_current_user)):
    """Returns recent push notifications for the user."""
    return [
        {
            "id": "n1",
            "title": "EURUSD Buy Signal",
            "severity": "info",
            "timestamp": "2023-10-01T10:00:00Z"
        }
    ]

@router.post("/workflows/{workflow_id}/approve")
async def approve_workflow(workflow_id: str, user: dict = Depends(get_current_user)):
    """Approves a pending automation workflow directly from the mobile app."""
    return {"status": "approved", "workflow_id": workflow_id}
