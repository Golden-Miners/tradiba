from tradiba.hermes.models.ollama import OllamaClient
from tradiba.hermes.research.experiments.orchestrator import ExperimentResult

class ResearchReflector:
    """Synthesizes learnings post-experiment for the Knowledge Graph."""
    
    def __init__(self, llm: OllamaClient):
        self.llm = llm

    async def synthesize(self, result: ExperimentResult, hypothesis_statement: str) -> str:
        prompt = (f"Hypothesis: {hypothesis_statement}\n"
                  f"Metrics: {result.metrics}\n"
                  "What did we learn from this experiment? Provide a brief summary.")
        system = "You are Hermes Research Agent. Keep reflections concise and factual."
        
        return await self.llm.generate(prompt=prompt, system=system)
