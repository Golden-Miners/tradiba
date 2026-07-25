from tradiba.performance.parallel import ParallelExecutor

def square(x: int) -> int:
    return x * x

def test_parallel_executor():
    executor = ParallelExecutor(max_workers=2)
    inputs = [1, 2, 3, 4, 5]
    
    results = executor.map(square, inputs)
    assert results == [1, 4, 9, 16, 25]
    
    tasks = [(square, (x,)) for x in inputs]
    submit_results = executor.submit_all(tasks)
    
    # ProcessPoolExecutor completion order is not guaranteed with as_completed
    assert sorted(submit_results) == [1, 4, 9, 16, 25]
