import uuid
from tradiba.workflows.engine import WorkflowEngine
from tradiba.workflows.models.workflow import Workflow, WorkflowStep

def test_workflow_engine():
    engine = WorkflowEngine()
    workflow_id = uuid.uuid4()
    workflow = Workflow(
        id=workflow_id,
        name="test_wf",
        version="v1",
        steps=[WorkflowStep("s1", "Step 1", "action", []), WorkflowStep("s2", "Step 2", "action", ["s1"])]
    )
    
    engine.start(workflow)
    state = engine._active_workflows[workflow_id]
    
    assert state["status"] == "running"
    assert state["current_step"] == 1
    
    engine.execute(workflow_id)
    assert state["status"] == "completed"
