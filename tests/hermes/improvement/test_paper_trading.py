"""Tests for Hermes Paper Trading Supervisor."""

from tradiba.hermes.improvement.evaluation.supervisor import PaperTradingSupervisor

def test_paper_trading_supervisor():
    supervisor = PaperTradingSupervisor({"max_drift": 0.05, "max_drawdown": 0.10})
    
    # Safe candidate
    assert supervisor.monitor({"drift": 0.02, "drawdown": 0.05}) is True
    
    # Unsafe drift
    assert supervisor.monitor({"drift": 0.06, "drawdown": 0.05}) is False
    
    # Unsafe drawdown
    assert supervisor.monitor({"drift": 0.02, "drawdown": 0.15}) is False
