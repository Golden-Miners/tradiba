from typing import Dict, Any

class ABTestingEngine:
    """
    Evaluates prompt versions, planning strategies, and reasoning workflows in isolated environments.
    """
    def __init__(self):
        self.experiments: Dict[str, Dict[str, Any]] = {}
        
    def start_experiment(self, experiment_id: str, variant_a: Any, variant_b: Any):
        self.experiments[experiment_id] = {
            "variant_a": variant_a,
            "variant_b": variant_b,
            "results_a": [],
            "results_b": []
        }
        
    def record_result(self, experiment_id: str, variant: str, score: float):
        if experiment_id in self.experiments:
            self.experiments[experiment_id][f"results_{variant}"].append(score)
            
    def get_winner(self, experiment_id: str) -> str:
        exp = self.experiments.get(experiment_id)
        if not exp:
            return "UNKNOWN"
            
        avg_a = sum(exp["results_a"]) / len(exp["results_a"]) if exp["results_a"] else 0
        avg_b = sum(exp["results_b"]) / len(exp["results_b"]) if exp["results_b"] else 0
        
        return "variant_a" if avg_a >= avg_b else "variant_b"
