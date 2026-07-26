from dataclasses import dataclass
from tradiba.aiops.recommendations import Recommendation
from tradiba.aiops.anomaly import Anomaly

@dataclass
class Explanation:
    observation: str
    evidence: str
    reasoning: str
    confidence: float
    recommended_action: str
    
    def render(self) -> str:
        return (
            f"Observation\n↓\n{self.observation}\n\n"
            f"Evidence\n↓\n{self.evidence}\n\n"
            f"Reasoning\n↓\n{self.reasoning}\n\n"
            f"Confidence\n↓\n{self.confidence}\n\n"
            f"Recommended Action\n↓\n{self.recommended_action}"
        )

class ExplainabilityEngine:
    """Ensures AI recommendations are traceable and verifiable."""
    def explain(self, anomaly: Anomaly, recommendation: Recommendation, reasoning_chain: str) -> Explanation:
        return Explanation(
            observation=anomaly.type,
            evidence=anomaly.evidence,
            reasoning=reasoning_chain,
            confidence=recommendation.confidence,
            recommended_action=recommendation.action
        )
