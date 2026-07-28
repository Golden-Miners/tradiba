from tradiba.hermes.federation.discovery.capability_registry import CapabilityRegistry

def test_discovery():
    reg = CapabilityRegistry()
    reg.advertise("cap1", {"version": "1.0"})
    assert len(reg.discover("cap1")) == 1
    assert len(reg.discover("cap2")) == 0
