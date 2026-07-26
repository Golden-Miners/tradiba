from enum import Enum, auto
from typing import Protocol, Any, Dict

class MarketRegime(Enum):
    TRENDING_UP = auto()
    TRENDING_DOWN = auto()
    RANGING = auto()
    EXPANDING = auto()
    CONTRACTING = auto()
    VOLATILE = auto()
    ACCUMULATION = auto()
    DISTRIBUTION = auto()
    MANIPULATION = auto()
    UNKNOWN = auto()

class RegimeClassifier(Protocol):
    """Protocol for market regime classifiers."""
    
    def classify(self, market_data: Any) -> MarketRegime:
        """Classify the current market regime based on data."""
        ...
        
    def get_confidence(self) -> float:
        """Return confidence score (0.0 to 1.0) of the current classification."""
        ...

class SimpleMovingAverageClassifier:
    """
    Reference Implementation: Simple Moving Average Regime Classifier.
    Classifies trend based on fast and slow moving averages.
    """
    
    def __init__(self, fast_period: int = 20, slow_period: int = 50, volatility_threshold: float = 0.02):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.volatility_threshold = volatility_threshold
        self._current_confidence = 0.0
        
    def classify(self, market_data: Dict[str, float]) -> MarketRegime:
        """
        Mock classification logic.
        Requires 'fast_ma', 'slow_ma', and 'current_volatility' in market_data dict.
        """
        if not market_data or "fast_ma" not in market_data or "slow_ma" not in market_data:
            self._current_confidence = 0.0
            return MarketRegime.UNKNOWN
            
        fast = market_data["fast_ma"]
        slow = market_data["slow_ma"]
        volatility = market_data.get("current_volatility", 0.0)
        
        # High volatility overrides trend
        if volatility > self.volatility_threshold:
            self._current_confidence = 0.8
            return MarketRegime.VOLATILE
            
        # Basic trend identification
        if fast > slow * 1.005:  # 0.5% buffer
            self._current_confidence = 0.7
            return MarketRegime.TRENDING_UP
        elif fast < slow * 0.995:
            self._current_confidence = 0.7
            return MarketRegime.TRENDING_DOWN
        else:
            self._current_confidence = 0.6
            return MarketRegime.RANGING

    def get_confidence(self) -> float:
        return self._current_confidence
