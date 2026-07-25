from tradiba.performance.memory import MemoryProfiler, MemoryPool

def test_memory_profiler():
    profiler = MemoryProfiler()
    profiler.start()
    
    # Allocate some memory
    _ = [x for x in range(100000)]
    
    profiler.stop()
    results = profiler.get_results()
    assert "current_mb" in results
    assert "peak_mb" in results
    assert results["peak_mb"] > 0

def test_memory_pool():
    class DummyItem:
        pass
        
    pool = MemoryPool(DummyItem)
    item1 = pool.acquire()
    assert isinstance(item1, DummyItem)
    
    pool.release(item1)
    item2 = pool.acquire()
    
    # Ensure it's the exact same object being reused
    assert item1 is item2
