import random
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class PredictiveAlert(BaseModel):
    service: str
    issue_type: str # e.g., 'degradation', 'exhaustion'
    confidence_score: float
    predicted_impact: str
    recommended_mitigation: str
    estimated_lead_time_minutes: int
    created_at: float = Field(default_factory=datetime.utcnow().timestamp)

class PredictiveOpsEngine:
    """Uses telemetry and historical data to predict operational issues before they occur."""

    def __init__(self):
        self.active_predictions: List[PredictiveAlert] = []

    def analyze_service_health(self, service: str, recent_telemetry: Dict[str, float]) -> Optional[PredictiveAlert]:
        """
        Analyze recent telemetry (latency, errors, queue depth) to predict issues.
        (Mock logic for demonstration)
        """
        latency = recent_telemetry.get("latency_ms", 0)
        error_rate = recent_telemetry.get("error_rate", 0)
        queue_depth = recent_telemetry.get("queue_depth", 0)

        alert = None

        if queue_depth > 1000 and latency > 200:
            alert = PredictiveAlert(
                service=service,
                issue_type="Message Queue Backlog",
                confidence_score=0.85,
                predicted_impact="Event processing delay causing downstream stale data",
                recommended_mitigation="Scale up worker pool or pause low-priority producers",
                estimated_lead_time_minutes=15
            )
        elif error_rate > 0.01:
             alert = PredictiveAlert(
                service=service,
                issue_type="Service Degradation",
                confidence_score=0.92,
                predicted_impact="High probability of cascading failure or SLA breach",
                recommended_mitigation="Initiate automated failover to standby replica",
                estimated_lead_time_minutes=5
            )
        
        if alert:
            self.active_predictions.append(alert)
        
        return alert

    def get_predictions(self) -> List[PredictiveAlert]:
        return self.active_predictions
