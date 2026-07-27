from tradiba.hermes.platform.twin.digital_twin import CognitiveDigitalTwin

def test_digital_twin():
    twin = CognitiveDigitalTwin()
    assert twin.run_simulation("s1", {})
