from typing import Dict, List, Tuple

class CorrelationIntelligence:
    """
    Reference Implementation: Correlation Intelligence.
    Analyzes strategy overlap to prevent over-concentration.
    """
    
    def __init__(self, correlation_matrix: Dict[Tuple[str, str], float]):
        """
        Mock initialization with a static correlation matrix.
        In a real scenario, this is derived from historical returns.
        """
        self.correlation_matrix = correlation_matrix
        
    def get_correlation(self, strategy_a: str, strategy_b: str) -> float:
        """Returns the correlation coefficient between two strategies."""
        # Check both orderings
        if (strategy_a, strategy_b) in self.correlation_matrix:
            return self.correlation_matrix[(strategy_a, strategy_b)]
        if (strategy_b, strategy_a) in self.correlation_matrix:
            return self.correlation_matrix[(strategy_b, strategy_a)]
        
        # Default to 0 correlation if unknown
        return 0.0
        
    def penalty_factor(self, strategy_id: str, existing_portfolio: List[str]) -> float:
        """
        Calculate a penalty factor (0.0 to 1.0) based on high correlation
        with existing strategies. Lower means more penalty.
        """
        if not existing_portfolio:
            return 1.0
            
        max_correlation = 0.0
        for existing in existing_portfolio:
            corr = self.get_correlation(strategy_id, existing)
            max_correlation = max(max_correlation, corr)
            
        # If highly correlated (>0.7), apply penalty
        if max_correlation > 0.7:
            return 0.5
        elif max_correlation > 0.5:
            return 0.8
        return 1.0
