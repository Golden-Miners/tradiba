from tradiba.hermes.learning.calibration.confidence import ConfidenceCalibrator

def test_confidence_calibration():
    calibrator = ConfidenceCalibrator()
    
    calibrator.record_prediction("pred_1", 0.8)
    calibrator.record_outcome("pred_1", 1.0)
    
    calibrator.record_prediction("pred_2", 0.5)
    calibrator.record_outcome("pred_2", 0.0)
    
    mace = calibrator.get_calibration_error()
    assert mace == 0.35  # (0.2 + 0.5) / 2
