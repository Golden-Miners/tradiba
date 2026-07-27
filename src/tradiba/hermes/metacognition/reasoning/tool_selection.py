from typing import Dict, List

class ToolSelectionOptimizer:
    """
    Ranks tools based on latency, cost, and historical success rates.
    """
    def __init__(self):
        self.tool_stats: Dict[str, Dict[str, float]] = {}
        
    def record_usage(self, tool_name: str, success: bool, latency: float):
        if tool_name not in self.tool_stats:
            self.tool_stats[tool_name] = {"uses": 0, "successes": 0, "total_latency": 0.0}
            
        stats = self.tool_stats[tool_name]
        stats["uses"] += 1
        if success:
            stats["successes"] += 1
        stats["total_latency"] += latency
        
    def rank_tools(self, available_tools: List[str]) -> List[str]:
        def score(t: str) -> float:
            if t not in self.tool_stats:
                return 0.5  # Neutral for unknown
            st = self.tool_stats[t]
            success_rate = st["successes"] / max(1, st["uses"])
            avg_latency = st["total_latency"] / max(1, st["uses"])
            # Higher score is better
            return success_rate - (avg_latency * 0.01)
            
        return sorted(available_tools, key=score, reverse=True)
