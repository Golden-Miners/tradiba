from tradiba.hermes.metacognition.memory.memory_optimizer import MemoryOptimizer

def test_memory_optimizer():
    opt = MemoryOptimizer()
    ctx = [
        {"key": "a", "val": 1},
        {"key": "a", "val": 2}, # newest
        {"key": "b", "val": 3}
    ]
    
    res = opt.optimize_context(ctx)
    assert len(res) == 2
    assert res[0]["val"] == 2
    assert res[1]["val"] == 3
