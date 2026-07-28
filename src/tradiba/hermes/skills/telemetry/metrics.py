from typing import Dict, Any, List

class SkillObservabilityTracker:
    """
    Skill observability tracking execution count, latency, failures, token/cost attribution.
    """
    def __init__(self):
        self.metrics: Dict[str, Dict[str, Any]] = {}

    def record_execution(self, skill_id: str, success: bool, latency_ms: float, tokens_used: int = 0) -> None:
        if skill_id not in self.metrics:
            self.metrics[skill_id] = {
                "total_executions": 0,
                "successes": 0,
                "failures": 0,
                "total_latency_ms": 0.0,
                "tokens_used": 0
            }

        m = self.metrics[skill_id]
        m["total_executions"] += 1
        if success:
            m["successes"] += 1
        else:
            m["failures"] += 1
        m["total_latency_ms"] += latency_ms
        m["tokens_used"] += tokens_used

    def get_metrics(self, skill_id: str) -> Dict[str, Any]:
        return self.metrics.get(skill_id, {})
