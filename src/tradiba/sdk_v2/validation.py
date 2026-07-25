from tradiba.sdk_v2.strategy import Strategy

def validate_strategy(strategy_cls: type) -> list[str]:
    """
    Static validation of a strategy class against SDK v2 requirements.
    Returns a list of error strings, or empty list if valid.
    """
    errors = []
    
    if not issubclass(strategy_cls, Strategy):
        errors.append("Class must inherit from tradiba.sdk_v2.strategy.Strategy")
        
    return errors
