import uuid
from tradiba.control_plane.deployment import DeploymentOrchestrator

def test_deployment_orchestrator():
    orchestrator = DeploymentOrchestrator()
    cluster_id = uuid.uuid4()
    
    record = orchestrator.schedule(cluster_id, "v2.5")
    assert record.status == "scheduled"
    
    orchestrator.complete(record.deployment_id)
    assert record.status == "completed"
    
    record2 = orchestrator.schedule(cluster_id, "v2.6")
    orchestrator.rollback(record2.deployment_id)
    assert record2.status == "rolled_back"
