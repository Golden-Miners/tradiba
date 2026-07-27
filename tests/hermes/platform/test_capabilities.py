from tradiba.hermes.platform.capabilities.registry import CognitiveCapabilityRegistry

def test_capabilities():
    registry = CognitiveCapabilityRegistry()
    registry.register("cap1", {"owner": "test"})
    assert registry.lookup("cap1")["owner"] == "test"
