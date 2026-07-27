from tradiba.hermes.hcos.memory.orchestrator import MemoryOrchestrator

def test_memory():
    mem = MemoryOrchestrator()
    mem.write_working_memory("k1", "v1")
    assert mem.read_working_memory("k1") == "v1"
    
    mem.store_episode({"desc": "market crash", "val": 1})
    res = mem.retrieve_episodes("crash")
    assert len(res) == 1
