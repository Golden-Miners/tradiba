def test_regime():
    """Verify regime aware allocation."""
    from tradiba.intelligence.regime import RegimeAwareAllocator
    from tradiba.intelligence.models.allocation import CapitalAllocation
    from tradiba.regimes.classifier import MarketRegime
    
    base_allocs = [CapitalAllocation("strat_1", 0.5, 100, {})]
    allocator = RegimeAwareAllocator(base_allocs)
    
    adjusted = allocator.adjust_for_regime(MarketRegime.VOLATILE)
    # Volatile halves allocation in our mock logic, then re-normalizes weight back to 1.0 because there is only 1 strategy
    assert adjusted[0].target_weight == 1.0
    assert adjusted[0].capital == 50.0
