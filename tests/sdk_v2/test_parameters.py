import pytest
from tradiba.sdk_v2.parameters import FloatParameter, IntParameter
from tradiba.sdk_v2.strategy import Strategy

class MyStrategy(Strategy):
    risk = FloatParameter(default=1.0, minimum=0.5, maximum=2.0)
    window = IntParameter(default=10, minimum=1, maximum=100)

def test_parameter_defaults():
    strat = MyStrategy()
    assert strat.risk == 1.0
    assert strat.window == 10

def test_parameter_validation():
    strat = MyStrategy()
    
    # Valid
    strat.risk = 1.5
    assert strat.risk == 1.5
    
    # Invalid minimum
    with pytest.raises(ValueError):
        strat.risk = 0.1
        
    # Invalid maximum
    with pytest.raises(ValueError):
        strat.window = 200

def test_parameter_extraction():
    strat = MyStrategy()
    strat.risk = 1.2
    
    params = strat.get_parameters()
    assert params["risk"] == 1.2
    assert params["window"] == 10
