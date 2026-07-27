from tradiba.hermes.world.predictions.framework import PredictionFramework

def test_prediction_framework():
    framework = PredictionFramework()
    
    risk = framework.forecast_risk({}, 10)
    assert risk["horizon"] == 10
    assert "confidence" in risk
    
    regime = framework.predict_regime({})
    assert "regime" in regime
    assert "probability" in regime
