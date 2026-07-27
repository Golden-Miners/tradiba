from tradiba.hermes.platform.memory.fabric import UnifiedMemoryFabric

def test_memory_fabric():
    fabric = UnifiedMemoryFabric()
    fabric.write("key1", "val1")
    assert fabric.read("key1") == "val1"
    assert fabric.read("key2") is None
