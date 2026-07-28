from tradiba.automation.sla.escalation_engine import SLAEngine

def test_sla():
    sla = SLAEngine()
    sla.register_sla("t1", 10)
    assert not sla.check_breach("t1", 5)
    assert sla.check_breach("t1", 15)
