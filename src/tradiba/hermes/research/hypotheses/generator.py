from tradiba.hermes.models.ollama import OllamaClient
from dataclasses import dataclass
import uuid

@dataclass
class Hypothesis:
    id: str
    topic_id: str
    statement: str
    version: int = 1

class HypothesisGenerator:
    """Synthesizes actionable hypotheses based on research topics."""
    
    def __init__(self, llm: OllamaClient):
        self.llm = llm

    async def generate(self, topic_description: str, topic_id: str) -> Hypothesis:
        prompt = f"Given the following research topic, generate a single, testable quantitative trading hypothesis:\nTopic: {topic_description}"
        system = "You are Hermes Research Agent. Formulate precise hypotheses focusing on features like entry logic, stop loss, or volatility."
        
        statement = await self.llm.generate(prompt=prompt, system=system)
        return Hypothesis(
            id=str(uuid.uuid4()),
            topic_id=topic_id,
            statement=statement.strip()
        )
