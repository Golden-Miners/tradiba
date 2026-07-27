from tradiba.hermes.metacognition.evaluator.reasoning_quality import ReasoningQualityAnalyzer

def test_reasoning_quality():
    analyzer = ReasoningQualityAnalyzer()
    plan = {"steps": ["a", "b"], "evidence": ["e1"]}
    metrics = analyzer.evaluate_plan("p1", plan)
    
    assert metrics["logical_consistency"] == 0.9
    assert metrics["evidence_coverage"] == 0.2
    assert metrics["efficiency"] == 0.5
