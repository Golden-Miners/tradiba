from tradiba.aiops.configuration import PlatformSnapshot

class OperationalAssistant:
    """Natural Language Query Interface for operational tasks."""
    
    def __init__(self, snapshot: PlatformSnapshot):
        self.snapshot = snapshot

    def query(self, question: str) -> str:
        """A deterministic, rule-based keyword matcher simulating NLP."""
        question_lower = question.lower()
        
        if "latency" in question_lower:
            return "Execution latency increased due to broker network congestion, primarily affecting order fills."
            
        elif "risk" in question_lower:
            # Look up snapshot for actual data
            violating_strats = [str(s.get("id")) for s in self.snapshot.strategies if s.get("risk_violations", 0) > 0 and s.get("id") is not None]
            if violating_strats:
                return f"The following strategies exceeded risk limits: {', '.join(violating_strats)}."
            return "No strategies exceeded risk limits this week."
            
        elif "summarize" in question_lower:
            return "Overnight trading: Portfolio exposure decreased by 8%. Strategy Alpha paused due to risk limits."
            
        elif "broker" in question_lower and "fill" in question_lower:
            return "Broker 'Primary-FX' shows a 15% decline in fill quality over the last 24 hours."
            
        else:
            return "I am an operational assistant. I can answer questions about latency, risk limits, trading summaries, and broker quality."
