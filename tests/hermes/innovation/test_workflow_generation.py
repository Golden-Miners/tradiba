from tradiba.hermes.innovation.generators.workflow_synthesizer import WorkflowSynthesizer

def test_workflow_generation():
    synth = WorkflowSynthesizer()
    flow = synth.synthesize(["Market", "Macro", "Risk"])
    
    assert flow["version"] == "1.0"
    assert len(flow["edges"]) == 2
    assert "Market -> Macro" in flow["edges"]
