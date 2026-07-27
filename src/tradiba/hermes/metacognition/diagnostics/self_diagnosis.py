from typing import Dict, Any, List

class SelfDiagnosisEngine:
    """
    Detects repeated planning failures, slow paths, and issues remediation recommendations.
    """
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        
    def record_execution(self, plan_id: str, success: bool, latency: float):
        self.history.append({
            "plan_id": plan_id,
            "success": success,
            "latency": latency
        })
        
    def run_diagnostics(self) -> List[str]:
        issues = []
        if not self.history:
            return issues
            
        success_rate = sum(1 for h in self.history if h["success"]) / len(self.history)
        if success_rate < 0.8:
            issues.append("High failure rate detected. Recommend deep analytical reasoning fallback.")
            
        avg_latency = sum(h["latency"] for h in self.history) / len(self.history)
        if avg_latency > 5.0:
            issues.append("High latency paths detected. Recommend caching or fast heuristic models.")
            
        return issues
