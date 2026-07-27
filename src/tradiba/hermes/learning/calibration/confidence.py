from typing import Dict, Any, List

class ConfidenceCalibrator:
    """
    Tracks Hermes's predicted confidence vs. actual outcomes and adjusts calibration trends.
    """
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        
    def record_prediction(self, prediction_id: str, predicted_confidence: float):
        self.history.append({
            "id": prediction_id,
            "predicted": predicted_confidence,
            "actual": None,
            "error": None
        })
        
    def record_outcome(self, prediction_id: str, actual_outcome: float):
        for record in self.history:
            if record["id"] == prediction_id:
                record["actual"] = actual_outcome
                record["error"] = abs(record["predicted"] - actual_outcome)
                break
                
    def get_calibration_error(self) -> float:
        """Returns the Mean Absolute Calibration Error (MACE)."""
        errors = [r["error"] for r in self.history if r["error"] is not None]
        if not errors:
            return 0.0
        return sum(errors) / len(errors)
