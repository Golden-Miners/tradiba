import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, List

from .metrics import OptimizationResult


@dataclass(slots=True)
class OptimizationReport:
    """Consolidated report for an optimization run."""
    best_result: OptimizationResult
    top_results: List[OptimizationResult]
    walk_forward: Dict[str, Any]
    monte_carlo: Dict[str, Any]
    recommendations: List[str]

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=4)
        
    def __str__(self) -> str:
        s = "--- OPTIMIZATION REPORT ---\n\n"
        s += "BEST PARAMETERS:\n"
        for k, v in self.best_result.parameters.items():
            s += f"  {k}: {v}\n"
            
        s += "\nBEST STATISTICS:\n"
        stats = asdict(self.best_result.statistics)
        for k, v in stats.items():
            s += f"  {k}: {v}\n"
            
        s += f"\nSCORE: {self.best_result.score}\n"
        
        s += "\nMONTE CARLO:\n"
        for k, v in self.monte_carlo.items():
            s += f"  {k}: {v}\n"
            
        s += "\nRECOMMENDATIONS:\n"
        for rec in self.recommendations:
            s += f"  - {rec}\n"
            
        return s
