
class SemanticMemory:
    """Stores permanent trading knowledge and platform rules."""
    def __init__(self):
        # In a production system, this would query a Vector DB (e.g. Chroma)
        self.knowledge_base = {
            "ICT": "Inner Circle Trader methodology focuses on Market Structure Shifts (MSS) and Fair Value Gaps (FVG).",
            "Risk": "Never risk more than 1% of the portfolio on a single trade. Max drawdown is 5%.",
            "SMC": "Smart Money Concepts tracks institutional order flow through Order Blocks."
        }

    def query(self, topic: str) -> str:
        """Simple keyword matching for v4.1."""
        results = []
        for key, value in self.knowledge_base.items():
            if key.lower() in topic.lower() or topic.lower() in key.lower():
                results.append(value)
        return " ".join(results) if results else "No relevant semantic knowledge found."
