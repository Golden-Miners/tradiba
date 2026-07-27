from tradiba.hermes.models.ollama import OllamaClient
from typing import List, Dict

class HermesConversation:
    """Handles chat-based queries and interfaces with the LLM."""
    
    def __init__(self, llm: OllamaClient):
        self.llm = llm
        self.history: List[Dict[str, str]] = [
            {"role": "system", "content": "You are Hermes, the cognitive trading advisor. Support all recommendations with evidence."}
        ]

    async def chat(self, user_message: str) -> str:
        self.history.append({"role": "user", "content": user_message})
        response = await self.llm.chat(self.history)
        self.history.append({"role": "assistant", "content": response})
        return response
