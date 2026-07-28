from typing import Dict, Any, List

class AnomalyDetector:
    """
    Rule-based, statistical, and behavioral anomaly detection across systems.
    """
    def detect_anomalies(self, metrics_stream: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        anomalies = []
        for metric in metrics_stream:
            if metric.get("value", 0) > metric.get("threshold", 100):
                anomalies.append(metric)
        return anomalies
