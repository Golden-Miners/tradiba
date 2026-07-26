def test_ensemble():
    """Verify ensemble behavior."""
    from tradiba.intelligence.ensemble import EnsembleDecisionEngine
    
    signals = [
        {"strategy_id": "1", "action": "BUY", "confidence": 0.9},
        {"strategy_id": "2", "action": "BUY", "confidence": 0.7},
        {"strategy_id": "3", "action": "SELL", "confidence": 0.8},
    ]
    
    engine = EnsembleDecisionEngine("majority_vote")
    result = engine.aggregate_signals(signals)
    assert result["action"] == "BUY"
    assert result["sources"] == 3
