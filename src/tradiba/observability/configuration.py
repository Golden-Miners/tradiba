import os
from typing import List


class ConfigurationError(Exception):
    pass


class ConfigValidator:
    """Validates required configuration/environment at startup."""
    
    @staticmethod
    def validate() -> None:
        errors: List[str] = []
        
        # Risk bounds
        risk_pct = float(os.getenv("TRADIBA_RISK_PCT", "1.0"))
        if not (0.0 < risk_pct <= 10.0):
            errors.append(f"Risk percentage {risk_pct} must be between 0 and 10.")
            
        # MT5 configuration
        # In a real setup, verify path or credentials
        if not os.getenv("MT5_PATH") and os.getenv("TRADIBA_ENV") == "production":
            errors.append("MT5_PATH not set in production.")
            
        if errors:
            raise ConfigurationError("\n".join(errors))
