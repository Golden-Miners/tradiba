import httpx
from typing import Dict, Any, List

class OllamaClient:
    """Client for interacting with local Ollama models."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen2:7b"):
        # The user mentioned Qwen 3 8B, but currently qwen2 is broadly available on ollama.
        # We will default to the model name requested or its closest equivalent.
        self.base_url = base_url
        self.model = model

    async def generate(self, prompt: str, system: str = "") -> str:
        async with httpx.AsyncClient() as client:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "system": system,
                "stream": False
            }
            response = await client.post(f"{self.base_url}/api/generate", json=payload)
            response.raise_for_status()
            return response.json().get("response", "")

    async def chat(self, messages: List[Dict[str, str]]) -> str:
        async with httpx.AsyncClient() as client:
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False
            }
            response = await client.post(f"{self.base_url}/api/chat", json=payload)
            response.raise_for_status()
            return response.json().get("message", {}).get("content", "")
