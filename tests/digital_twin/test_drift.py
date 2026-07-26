from tradiba.digital_twin.drift import DriftDetector

def test_drift_detection():
    detector = DriftDetector()
    
    prod_state = {"portfolio": {"cash": 1000}}
    twin_state_good = {"portfolio": {"cash": 1005}}
    twin_state_bad = {"portfolio": {"cash": 500}}
    
    assert len(detector.detect_drift(prod_state, twin_state_good)) == 0
    
    drifts = detector.detect_drift(prod_state, twin_state_bad)
    assert len(drifts) == 1
    assert drifts[0]["type"] == "portfolio_drift"
    assert drifts[0]["severity"] == "HIGH"
