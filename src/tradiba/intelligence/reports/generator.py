from typing import Dict, Any, List
from tradiba.intelligence.models.allocation import CapitalAllocation

class IntelligenceReportGenerator:
    """
    Reference Implementation: Intelligence Reports.
    Generates reports on portfolio composition and strategy allocation.
    """
    
    def generate_portfolio_composition(self, allocations: List[CapitalAllocation]) -> Dict[str, Any]:
        """Generate a breakdown of the current portfolio."""
        report: Dict[str, Any] = {
            "total_strategies": len(allocations),
            "allocations": []
        }
        
        for alloc in allocations:
            report["allocations"].append({
                "strategy_id": alloc.strategy_id,
                "weight_pct": round(alloc.target_weight * 100, 2),
                "capital": alloc.capital
            })
            
        return report
