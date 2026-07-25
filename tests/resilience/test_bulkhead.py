import time
from tradiba.resilience.bulkhead import Bulkhead

def test_bulkhead():
    bulkhead = Bulkhead("test_bulkhead", max_workers=2)
    
    def slow_op():
        time.sleep(0.1)
        return "done"
        
    future1 = bulkhead.execute(slow_op)
    future2 = bulkhead.execute(slow_op)
    
    assert future1.result() == "done"
    assert future2.result() == "done"
    
    bulkhead.shutdown()
