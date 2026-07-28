from tradiba.hermes.multimodal.vision.intelligence import VisionIntelligence

def test_vision():
    vi = VisionIntelligence()
    res = vi.analyze_chart(b"image")
    assert "head_and_shoulders" in res["patterns"]
    assert vi.detect_anomalies(b"image") == ["liquidity_void"]
