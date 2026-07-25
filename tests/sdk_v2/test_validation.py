from tradiba.sdk_v2.validation import validate_strategy
from tradiba.sdk_v2.strategy import Strategy

class GoodStrat(Strategy):
    pass

class BadStrat:
    pass

def test_validation():
    errors = validate_strategy(GoodStrat)
    assert len(errors) == 0
    
    errors = validate_strategy(BadStrat)
    assert len(errors) == 1
    assert "Strategy" in errors[0]
