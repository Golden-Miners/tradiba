from tradiba.hermes.engineering.analysis.intelligence import CodeIntelligenceEngine

def test_analysis():
    engine = CodeIntelligenceEngine()
    res = engine.analyze_module("test_module")
    assert res["module"] == "test_module"
    assert "complexity" in res
