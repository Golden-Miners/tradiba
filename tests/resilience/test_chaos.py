import pytest
from tradiba.resilience.chaos import ChaosExperiment
from tradiba.resilience.exceptions import ChaosInjectedError

def test_chaos_experiment_disabled():
    chaos = ChaosExperiment("test_chaos", enabled=False)
    
    def simple_op():
        return "success"
        
    result = chaos.run(simple_op)
    assert result == "success"

def test_chaos_experiment_enabled(monkeypatch):
    chaos = ChaosExperiment("test_chaos", enabled=True)
    
    def simple_op():
        return "success"
        
    # Force exception branch
    monkeypatch.setattr("tradiba.resilience.chaos.random.random", lambda: 0.01)
    
    with pytest.raises(ChaosInjectedError):
        chaos.run(simple_op)
        
    # Force latency branch
    monkeypatch.setattr("tradiba.resilience.chaos.random.random", lambda: 0.1)
    monkeypatch.setattr("tradiba.resilience.chaos.time.sleep", lambda x: None)
    
    result = chaos.run(simple_op)
    assert result == "success"
