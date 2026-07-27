from typing import List, Dict, Any

class AIWorkflowSDK:
    """
    Composes reusable AI workflows using DAG primitives.
    """
    def __init__(self):
        self.workflows: Dict[str, List[str]] = {}
        
    def create_workflow(self, name: str, steps: List[str]):
        self.workflows[name] = steps
        
    def execute(self, name: str, initial_state: Any) -> Any:
        if name not in self.workflows:
            raise ValueError("Workflow not found")
            
        state = initial_state
        for step in self.workflows[name]:
            state = f"{state} -> {step}"
            
        return state
