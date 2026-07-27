from tradiba.hermes.innovation.registry.innovation_registry import InnovationRegistry

def test_registry():
    reg = InnovationRegistry()
    reg.register("prop1", "AGENT", {"name": "TestAgent"})
    
    reg.update_status("prop1", "SIMULATION")
    reg.update_status("prop1", "APPROVED")
    
    history = reg.get_lineage("prop1")
    assert len(history) == 3
    assert history == ["REGISTERED", "SIMULATION", "APPROVED"]
