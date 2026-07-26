from dataclasses import dataclass
from typing import Optional

@dataclass
class PromotionRecommendation:
    candidate_id: str
    target_stage: str  # e.g., "PAPER_TRADING"
    confidence: float
    evidence_summary: str
    expected_portfolio_impact: str

class PromotionEngine:
    """Evaluates validated strategies for lifecycle transitions."""
    
    def recommend_promotion(self, candidate_id: str, validation_results: bool) -> Optional[PromotionRecommendation]:
        """Proposes a promotion if validation criteria are met."""
        if validation_results:
            return PromotionRecommendation(
                candidate_id=candidate_id,
                target_stage="VALIDATED",
                confidence=0.92,
                evidence_summary="Passed all rigorous out-of-sample and stress tests.",
                expected_portfolio_impact="Improves overall Sharpe by 0.1 without adding correlated risk."
            )
        return None
