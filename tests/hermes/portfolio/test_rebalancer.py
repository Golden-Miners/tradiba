import datetime
from tradiba.hermes.portfolio.rebalancer.autonomous_rebalancer import AutonomousRebalancer

def test_regime_change_trigger():
    rebalancer = AutonomousRebalancer({})
    current_date = datetime.datetime(2023, 1, 1)
    rebalancer.last_rebalance = current_date
    
    assert rebalancer.should_rebalance(current_date, "bear", "bull", {})
    assert not rebalancer.should_rebalance(current_date, "bull", "bull", {})

def test_strategy_degradation_trigger():
    rebalancer = AutonomousRebalancer({})
    current_date = datetime.datetime(2023, 1, 1)
    rebalancer.last_rebalance = current_date
    
    # -16% drawdown triggers rebalance
    assert rebalancer.should_rebalance(current_date, "bull", "bull", {"s1": -0.16})
    assert not rebalancer.should_rebalance(current_date, "bull", "bull", {"s1": -0.10})

def test_scheduled_trigger():
    rebalancer = AutonomousRebalancer({"rebalance_interval_days": 30})
    rebalancer.execute_rebalance(datetime.datetime(2023, 1, 1))
    
    assert not rebalancer.should_rebalance(datetime.datetime(2023, 1, 15), "bull", "bull", {})
    assert rebalancer.should_rebalance(datetime.datetime(2023, 2, 2), "bull", "bull", {})
