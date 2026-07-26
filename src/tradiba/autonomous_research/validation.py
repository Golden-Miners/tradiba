from typing import Dict, Any

class ValidationFramework:
    """Evaluates strategy candidates across multiple validation stages."""
    
    def validate(self, experiment_results: Dict[str, Any]) -> bool:
        """
        Applies configurable acceptance criteria to experiment results.
        Stages: Statistical significance, Walk-forward stability, Regime robustness, etc.
        """
        results = experiment_results.get("results", {})
        
        # Mock acceptance criteria
        if results.get("sharpe_ratio", 0) > 1.2 and results.get("max_drawdown", 1) < 0.15:
            return True
            
        return False
