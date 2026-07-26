from tradiba.autonomous_research.meta_analysis import MetaAnalysisEngine

def test_meta_analysis():
    engine = MetaAnalysisEngine()
    
    experiments = [
        {"results": {"sharpe_ratio": 1.5}},
        {"results": {"sharpe_ratio": 0.5}},
    ]
    
    analysis = engine.analyze_experiments(experiments)
    assert analysis["total_analyzed"] == 2
    assert analysis["success_rate"] == 0.5
