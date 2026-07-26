from tradiba.digital_twin.scenarios import ScenarioLab

def test_scenario_execution():
    lab = ScenarioLab()
    
    scenario = {"name": "replace_broker"}
    baseline = {"cash": 1000}
    
    result = lab.run_scenario(scenario, baseline)
    assert result["scenario"] == "replace_broker"
    assert result["risk_status"] == "acceptable"
