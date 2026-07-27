from tradiba.hermes.models.ollama import OllamaClient

class Reflector:
    """Evaluates task outcomes and updates memory."""
    def __init__(self, llm_client: OllamaClient):
        self.llm = llm_client

    async def reflect(self, goal_description: str, outcome: str) -> str:
        prompt = f"Goal: {goal_description}\nOutcome: {outcome}\nReflect on what succeeded, what failed, and what should improve."
        system = "You are Hermes. Write a critical reflection report on the trading outcome."
        return await self.llm.generate(prompt=prompt, system=system)
