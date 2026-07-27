
class AdaptiveReasoningStrategies:
    """
    Selects reasoning approaches based on task complexity.
    """
    def __init__(self):
        self.strategies = {
            "fast_heuristic": "Use simple rules, bypass deep generation",
            "deep_analytical": "Use Chain of Thought, fetch full context",
            "risk_first": "Analyze risk vectors before any planning"
        }
        
    def select_strategy(self, task_type: str, urgency: str) -> str:
        if urgency == "HIGH":
            return "fast_heuristic"
        if task_type == "PORTFOLIO_ROTATION":
            return "deep_analytical"
        if task_type == "EMERGENCY_EXIT":
            return "risk_first"
        return "fast_heuristic"
