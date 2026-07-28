from tradiba.operations.root_cause.rca_engine import RCAEngine

def test_rca():
    rca = RCAEngine()
    res = rca.analyze({"incident_id": "i1"})
    assert res["incident"] == "i1"
    assert "root_cause" in res
