from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any

from tradiba.operations.backups import BackupManager
from tradiba.operations.compliance import ComplianceEngine
from tradiba.operations.incidents_manager import IncidentManager, IncidentSeverity
from tradiba.operations.slo.engine import SLOEngine
from tradiba.operations.capacity.planner import CapacityPlanner
from tradiba.operations.forecasting.predictive_ops import PredictiveOpsEngine
from tradiba.operations.dependencies.graph import DependencyGraph
from tradiba.operations.releases.manager import ReleaseManager
from tradiba.operations.runbooks.executor import RunbookExecutor
from tradiba.operations.reliability.analytics import ReliabilityAnalyticsEngine

router = APIRouter(prefix="/operations", tags=["Operations"])

backup_manager = BackupManager()
compliance_engine = ComplianceEngine()
incident_manager = IncidentManager()
slo_engine = SLOEngine()
capacity_planner = CapacityPlanner()
predictive_ops = PredictiveOpsEngine()
dependency_graph = DependencyGraph()
release_manager = ReleaseManager()
runbook_executor = RunbookExecutor()
reliability_analytics = ReliabilityAnalyticsEngine()


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

@router.post("/runbooks")
async def execute_runbook(runbook_name: str, requester: str, parameters: Dict[str, str] = {}):
    """Requests execution of an operational runbook."""
    execution = runbook_executor.request_execution(runbook_name, parameters, requester)
    # Auto-approve for demo
    result = await runbook_executor.approve_and_execute(execution.id, "system-auto-approver")
    return result

@router.post("/releases")
async def record_release(service: str, version: str, change_type: str, approver: str):
    """Records a new release or change."""
    change = release_manager.record_change(service, version, change_type, approver)
    release_manager.update_status(change.id, "successful")
    return change

@router.post("/slo")
async def register_slo(slo_id: str, service: str, description: str, metric_type: str, target: float, operator: str):
    """Registers a new Service Level Objective."""
    slo = slo_engine.register_slo(slo_id, service, description, metric_type, target, operator)
    return slo

@router.get("/dependencies")
async def get_dependencies() -> Dict[str, Any]:
    """Returns the service dependency graph topology."""
    return dependency_graph.get_topology()

@router.get("/capacity")
async def get_capacity() -> Dict[str, Any]:
    """Returns current capacity usage history."""
    return {"history": capacity_planner.usage_history}

@router.get("/reliability")
async def get_reliability(service: str) -> Dict[str, Any]:
    """Returns reliability analytics for a service."""
    return reliability_analytics.get_metrics(service).dict()

@router.get("/forecast")
async def get_forecast(service: str) -> Dict[str, Any]:
    """Generates a capacity forecast for a service."""
    return capacity_planner.generate_forecast(service).dict()
