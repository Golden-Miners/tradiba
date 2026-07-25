from tradiba.research.regime import RegimeDetector

def test_regime_detection():
    detector = RegimeDetector()
    
    # Stub test
    regime = detector.detect({"market": "data"})
    assert regime == "trending"
