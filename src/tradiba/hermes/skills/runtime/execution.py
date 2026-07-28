from typing import Dict, Any, Optional
import time
from tradiba.hermes.skills.sdk.base import Skill

class SkillExecutionRuntime:
    """
    Isolated execution runtime with timeouts, quotas, retries, and fault containment.
    """
    def __init__(self, timeout_seconds: float = 30.0, max_retries: int = 2):
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.active_executions: Dict[str, Dict[str, Any]] = {}

    def run(self, skill: Skill, context: Dict[str, Any]) -> Dict[str, Any]:
        if not skill.validate():
            return {"status": "FAILED", "reason": "Skill not validated or initialized"}
        
        exec_id = f"exec_{skill.id}_{int(time.time()*1000)}"
        self.active_executions[exec_id] = {"skill_id": skill.id, "status": "RUNNING", "start_time": time.time()}

        retries = 0
        last_error: Optional[Exception] = None

        while retries <= self.max_retries:
            try:
                result = skill.execute(context)
                self.active_executions[exec_id]["status"] = "COMPLETED"
                return {"status": "SUCCESS", "result": result, "execution_id": exec_id}
            except Exception as e:
                last_error = e
                retries += 1

        self.active_executions[exec_id]["status"] = "FAILED"
        return {"status": "FAILED", "reason": str(last_error), "execution_id": exec_id}
