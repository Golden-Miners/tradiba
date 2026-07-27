"""Tests for Hermes Reward Metrics."""

from tradiba.hermes.improvement.rewards.metrics import RewardFramework

def test_reward_metrics_evaluate():
    rewards = RewardFramework()
    results = {
        "net_return": 15.5,
        "sharpe_ratio": 1.2,
        "max_drawdown": 0.05,
        "win_rate": 0.6
    }
    
    evaluation = rewards.evaluate(results)
    assert evaluation["net_return"] == 15.5
    assert evaluation["sharpe_ratio"] == 1.2
    assert evaluation["max_drawdown"] == 0.05
    assert evaluation["win_rate"] == 0.6
    assert evaluation["consistency"] == 1.0  # default
