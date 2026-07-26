from typing import Dict, Any, List

class AIInsightService:
    """Serves market narratives and recommended strategies."""
    
    def get_insights(self) -> List[Dict[str, Any]]:
        return [
            {
                "narrative": "Bullish expansion",
                "regime": "High Volatility",
                "recommended_strategy": "MomentumBreakout",
                "confidence": 0.9,
                "evidence_link": "decision_123"
            }
        ]
