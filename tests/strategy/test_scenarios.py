from tradiba.strategy.scenarios.simulator import EnterpriseScenarioSimulator

def test_scenarios():
    sim = EnterpriseScenarioSimulator()
    res = sim.simulate("crash", {})
    assert res["scenario"] == "crash"
