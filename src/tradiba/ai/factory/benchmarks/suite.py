from typing import Dict

class BenchmarkSuite:
    """
    Standardized benchmarks for tracking regression across versions.
    """
    def __init__(self):
        self.results: Dict[str, Dict[str, float]] = {}
        
    def run_benchmark(self, model_version: str, dataset_version: str) -> Dict[str, float]:
        # Simulate benchmark run
        score = {"overall_score": 0.88, "latency_ms": 150.0}
        self.results[f"{model_version}_{dataset_version}"] = score
        return score
