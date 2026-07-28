from tradiba.automation.digital_twin.simulator import OperationalTwin

def test_digital_twin():
    twin = OperationalTwin()
    assert twin.simulate_workflow("w1", {})["status"] == "simulated"
