from tradiba.knowledge.provenance.engine import ProvenanceEngine

def test_provenance():
    engine = ProvenanceEngine()
    engine.record_provenance("k1", {"author": "alice"})
    res = engine.get_provenance("k1")
    assert res["author"] == "alice"
