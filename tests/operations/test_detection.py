from tradiba.operations.detection.anomaly_detector import AnomalyDetector

def test_detection():
    detector = AnomalyDetector()
    anoms = detector.detect_anomalies([{"value": 150, "threshold": 100}, {"value": 50, "threshold": 100}])
    assert len(anoms) == 1
    assert anoms[0]["value"] == 150
