def test_lifecycle():
    """Verify lifecycle transitions require the configured approvals."""
    from tradiba.intelligence.lifecycle import StrategyLifecycleManager
    from tradiba.intelligence.governance import StandardGovernance
    from tradiba.intelligence.models.strategy_descriptor import StrategyDescriptor, StrategyStatus
    
    gov = StandardGovernance()
    manager = StrategyLifecycleManager(gov)
    
    strat = StrategyDescriptor("strat_1", "test", "v1", "author", "low", [], [])
    
    # Can't jump straight to PRODUCTION from EXPERIMENTAL
    assert manager.promote(strat, StrategyStatus.PRODUCTION) is False
    assert strat.status == StrategyStatus.EXPERIMENTAL
    
    # Must be PAPER_TRADING first
    strat.status = StrategyStatus.PAPER_TRADING
    assert manager.promote(strat, StrategyStatus.PRODUCTION) is True
    assert strat.status == StrategyStatus.PRODUCTION
