from dataclasses import dataclass

@dataclass(slots=True)
class AnalyticsConfig:
    """
    Configuration for the portfolio and risk analytics engine.
    """
    default_confidence_level: float = 0.95
    historical_lookback_days: int = 252
    base_currency: str = "USD"
