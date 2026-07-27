from tradiba.hermes.hcos.resources.manager import ResourceManager

def test_resource_manager():
    mgr = ResourceManager({"tokens": 1000})
    
    assert mgr.consume("tokens", 500) == True
    assert mgr.consume("tokens", 600) == False
    
    mgr.release("tokens", 500)
    assert mgr.consume("tokens", 600) == True
