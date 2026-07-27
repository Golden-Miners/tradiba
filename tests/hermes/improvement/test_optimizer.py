"""Tests for Hermes Improvement Optimizer."""

from tradiba.hermes.improvement.optimizer.engine import SelfImprovementEngine

def test_engine_select_candidate():
    engine = SelfImprovementEngine()
    candidate = engine.select_candidate("strat_1")
    assert candidate["strategy_id"] == "strat_1"
    assert candidate["status"] == "selected"

def test_engine_generate_proposal():
    engine = SelfImprovementEngine()
    proposal = engine.generate_proposal({"strategy_id": "strat_1"})
    assert proposal["strategy_id"] == "strat_1"
    assert proposal["proposal"] == "test_proposal"

def test_engine_execute_optimization():
    engine = SelfImprovementEngine()
    result = engine.execute_optimization({"strategy_id": "strat_1"})
    assert result["optimized"] is True
    assert "timestamp" in result

def test_engine_compare_baseline():
    engine = SelfImprovementEngine()
    assert engine.compare_baseline({"id": "old"}, {"id": "new"}) is True
