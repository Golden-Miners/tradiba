import pytest
from tradiba.hermes.live.policies.engine import PolicyEngine

@pytest.fixture
def policy_engine():
    policies = {
        "allowed_instruments": ["BTC/USD", "ETH/USD"],
        "approved_strategies": ["trend_following", "mean_reversion"],
        "min_confidence": 0.8,
        "max_position_size": 1.5,
        "max_concurrent_trades": 3,
        "max_daily_loss": 500.0
    }
    return PolicyEngine(policies)

def test_policy_engine_approved(policy_engine):
    proposal = {
        "symbol": "BTC/USD",
        "strategy": "trend_following",
        "size": 1.0,
        "confidence": 0.85
    }
    current_state = {
        "active_trades_count": 1,
        "daily_loss": 100.0
    }
    assert policy_engine.evaluate_proposal(proposal, current_state) is True

def test_policy_engine_invalid_instrument(policy_engine):
    proposal = {
        "symbol": "SOL/USD",
        "strategy": "trend_following",
        "size": 1.0,
        "confidence": 0.85
    }
    current_state = {}
    assert policy_engine.evaluate_proposal(proposal, current_state) is False

def test_policy_engine_low_confidence(policy_engine):
    proposal = {
        "symbol": "BTC/USD",
        "strategy": "trend_following",
        "size": 1.0,
        "confidence": 0.7
    }
    current_state = {}
    assert policy_engine.evaluate_proposal(proposal, current_state) is False

def test_policy_engine_max_concurrent_breach(policy_engine):
    proposal = {
        "symbol": "BTC/USD",
        "strategy": "trend_following",
        "size": 1.0,
        "confidence": 0.9
    }
    current_state = {
        "active_trades_count": 3
    }
    assert policy_engine.evaluate_proposal(proposal, current_state) is False
