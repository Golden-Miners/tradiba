from tradiba.hermes.models.ollama import OllamaClient
from tradiba.hermes.memory.long_term_memory import LongTermMemory

class Learner:
    """Processes backtests and simulations into long-term insights."""
    
    def __init__(self, llm: OllamaClient, ltm: LongTermMemory):
        self.llm = llm
        self.ltm = ltm
        
    async def analyze_research(self, topic: str, raw_data: str) -> str:
        """Analyzes a research report and archives insights into Long-Term Memory."""
        prompt = f"Analyze the following research data on {topic} and extract the key actionable insights:\n{raw_data}"
        system = "You are Hermes' Learning Engine. Output concise, factual trading insights."
        
        insights = await self.llm.generate(prompt=prompt, system=system)
        
        # Save to Long-Term Memory
        self.ltm.archive_research(topic, insights)
        return insights
