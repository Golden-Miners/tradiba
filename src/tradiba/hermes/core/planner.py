from typing import List, Dict, Any
from .goals import HermesGoal
from tradiba.hermes.models.ollama import OllamaClient

class Planner:
    """Generates execution plans based on high-level goals."""
    def __init__(self, llm_client: OllamaClient):
        self.llm = llm_client

    async def generate_plan(self, goal: HermesGoal) -> List[str]:
        prompt = f"Create a step-by-step trading research plan for the following goal: {goal.description}"
        system = "You are Hermes, an expert trading AI advisor. Output only a numbered list of steps."
        response = await self.llm.generate(prompt=prompt, system=system)
        
        # Simple parse: split by newlines and filter out empty strings
        steps = [step.strip() for step in response.split("\n") if step.strip()]
        return steps
