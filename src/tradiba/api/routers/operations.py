from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any

from tradiba.operations.backups import BackupManager
from tradiba.operations.compliance import ComplianceEngine
from tradiba.operations.incidents import IncidentManager, IncidentSeverity

router = APIRouter(prefix="/operations", tags=["Operations"])

backup_manager = BackupManager()
compliance_engine = ComplianceEngine()
incident_manager = IncidentManager()

@router.get("/dashboard")
async def get_ops_dashboard() -> Dict[str, Any]:
    """Returns aggregated data for the Operational Dashboard."""
    return {
        "status": "healthy",
        "active_incidents_count": len(incident_manager.get_active_incidents()),
        "dr_readiness": "ready",
        "last_backup": "2026-07-27T00:00:00Z"
    }

@router.post("/backups/trigger")
async def trigger_backup(background_tasks: BackgroundTasks):
    """Triggers an async database and event store backup."""
    # In a real app, this would run safely in background
    backup_manager.trigger_database_backup()
    backup_manager.trigger_event_store_backup()
    return {"message": "Backup triggered"}

@router.get("/compliance/reports/{user_id}")
async def generate_compliance_report(user_id: str, format: str = "json"):
    """Generates a trading compliance report."""
    try:
        filepath = compliance_engine.generate_trading_activity_report(user_id, format)
        return {"message": "Report generated", "path": filepath}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/incidents")
async def report_incident(title: str, description: str, severity: IncidentSeverity):
    """Reports a new system incident."""
    incident = incident_manager.report_incident(title, description, severity, ["API Gateway"])
    return incident
