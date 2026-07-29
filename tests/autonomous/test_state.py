from tradiba.autonomous.enterprise_state.engine import UnifiedEnterpriseStateEngine

def test_state():
    engine = UnifiedEnterpriseStateEngine()
    engine.update_state("markets", {"status": "open"})
    assert engine.get_state("markets")["status"] == "open"
