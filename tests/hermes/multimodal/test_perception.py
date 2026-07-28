from tradiba.hermes.multimodal.perception.engine import MultimodalPerceptionEngine

def test_perception():
    engine = MultimodalPerceptionEngine()
    assert engine.detect_format(b"%PDF-1.4") == "pdf"
    assert engine.detect_format(b"1234") == "binary"
    assert engine.ingest("file.txt", "text")["format"] == "text"
