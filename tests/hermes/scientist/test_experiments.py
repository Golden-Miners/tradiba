from tradiba.hermes.scientist.experiments.designer import ExperimentDesigner

def test_experiments():
    designer = ExperimentDesigner()
    exp = designer.design_experiment("e1", "h1")
    assert exp["hypothesis_id"] == "h1"
    assert exp["control_group"] == "A"
