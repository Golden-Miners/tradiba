from tradiba.ai.factory.registry.artifact_registry import AIFactoryRegistry

def test_registry():
    registry = AIFactoryRegistry()
    registry.register_artifact("model", "m1", {"provider": "openai"})
    assert registry.get_artifact("model", "m1")["provider"] == "openai"
