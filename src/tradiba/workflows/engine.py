import uuid
from typing import Any
from tradiba.workflows.models.workflow import Workflow
from tradiba.workflows.exceptions import InvalidStateTransitionError

class WorkflowEngine:
    """Coordinates workflow state transitions and dependencies."""
    def __init__(self) -> None:
        self._active_workflows: dict[uuid.UUID, dict[str, Any]] = {}
        
    def start(self, workflow: Workflow) -> None:
        self._active_workflows[workflow.id] = {
            "workflow": workflow,
            "status": "running",
            "current_step": 0
        }
        self.execute(workflow.id)

    def execute(self, workflow_id: uuid.UUID) -> None:
        if workflow_id not in self._active_workflows:
            raise InvalidStateTransitionError(f"Workflow {workflow_id} not found.")
        
        state = self._active_workflows[workflow_id]
        if state["status"] != "running":
            raise InvalidStateTransitionError(f"Cannot execute workflow in state {state['status']}")
            
        workflow: Workflow = state["workflow"]
        current_step_idx = state["current_step"]
        
        if current_step_idx < len(workflow.steps):
            # Advance step
            state["current_step"] += 1
            if state["current_step"] >= len(workflow.steps):
                state["status"] = "completed"
        
    def pause(self, workflow_id: uuid.UUID) -> None:
        state = self._active_workflows.get(workflow_id)
        if state and state["status"] == "running":
            state["status"] = "paused"
            
    def resume(self, workflow_id: uuid.UUID) -> None:
        state = self._active_workflows.get(workflow_id)
        if state and state["status"] == "paused":
            state["status"] = "running"
            
    def cancel(self, workflow_id: uuid.UUID) -> None:
        state = self._active_workflows.get(workflow_id)
        if state and state["status"] in ["running", "paused"]:
            state["status"] = "cancelled"
