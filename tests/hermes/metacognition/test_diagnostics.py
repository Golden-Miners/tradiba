from tradiba.hermes.metacognition.diagnostics.self_diagnosis import SelfDiagnosisEngine

def test_diagnostics():
    engine = SelfDiagnosisEngine()
    engine.record_execution("p1", False, 1.0)
    engine.record_execution("p2", False, 10.0)
    
    issues = engine.run_diagnostics()
    assert len(issues) == 2
    assert any("failure rate" in i for i in issues)
    assert any("latency" in i for i in issues)
