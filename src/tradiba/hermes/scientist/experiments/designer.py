from typing import Dict, Any

class ExperimentDesigner:
    """
    Constructs reproducible experiments.
    """
    def __init__(self):
        self.experiments: Dict[str, Dict[str, Any]] = {}
        
    def design_experiment(self, exp_id: str, hypothesis_id: str) -> Dict[str, Any]:
        exp = {
            "hypothesis_id": hypothesis_id,
            "control_group": "A",
            "candidate_group": "B",
            "metrics": ["profitability", "latency"]
        }
        self.experiments[exp_id] = exp
        return exp
