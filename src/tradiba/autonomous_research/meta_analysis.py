from typing import List, Dict, Any

class MetaAnalysisEngine:
    """Synthesizes outcomes across many experiment runs to identify broader trends."""
    
    def analyze_experiments(self, past_experiments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Identifies feature importance trends, regime-specific performance, and parameter sensitivity.
        """
        # Mock analysis
        successful_runs = [exp for exp in past_experiments if exp.get("results", {}).get("sharpe_ratio", 0) > 1.0]
        
        return {
            "total_analyzed": len(past_experiments),
            "success_rate": len(successful_runs) / len(past_experiments) if past_experiments else 0,
            "key_finding": "High volatility regimes correlate with stronger momentum breakouts."
        }
