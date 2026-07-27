from tradiba.hermes.models.ollama import OllamaClient
from tradiba.hermes.research.experiments.orchestrator import ExperimentResult

class SelfEvaluator:
    """Critiques experiment statistical significance and efficiency."""
    
    def __init__(self, llm: OllamaClient):
        self.llm = llm

    async def evaluate(self, result: ExperimentResult) -> bool:
        """Evaluates if the experiment metrics justify a formal recommendation."""
        # Simple threshold for v4.2
        if result.metrics.get("sharpe_ratio", 0) > 1.2 and result.metrics.get("max_drawdown", 100) < 5.0:
            return True
        return False
