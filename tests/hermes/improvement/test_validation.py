"""Tests for Hermes Validation Pipeline."""

from tradiba.hermes.improvement.validation.pipeline import ValidationPipeline

def test_validation_pipeline_success():
    pipeline = ValidationPipeline()
    candidate = {"id": "strat_1"}
    
    assert pipeline.run_backtest(candidate) is True
    assert pipeline.run_walk_forward(candidate) is True
    assert pipeline.run_monte_carlo(candidate) is True
    assert pipeline.validate_candidate(candidate) is True
