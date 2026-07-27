from tradiba.hermes.scientist.publications.engine import PublicationEngine

def test_publications():
    engine = PublicationEngine()
    rep = engine.publish("Test", {"res": 1})
    assert "Test" in rep
    assert "res" in rep
