from typing import Dict, Any, List
from datetime import datetime

class DriftDetector:
    """Calculates state divergence between production and the twin."""
    
    def detect_drift(self, prod_state: Dict[str, Any], twin_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Identifies position drift, configuration drift, etc.
        """
        drifts = []
        prod_cash = prod_state.get("portfolio", {}).get("cash", 0)
        twin_cash = twin_state.get("portfolio", {}).get("cash", 0)
        
        if abs(prod_cash - twin_cash) > 100:
            drifts.append({
                "type": "portfolio_drift",
                "severity": "HIGH",
                "timestamp": datetime.utcnow().isoformat(),
                "suggested_investigation": "Check recent fill allocations."
            })
            
        return drifts
