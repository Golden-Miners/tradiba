from tradiba.modelops.registry.manager import ModelRegistryManager

def test_registry():
    registry = ModelRegistryManager()
    assert registry.register_model("m1", {})
