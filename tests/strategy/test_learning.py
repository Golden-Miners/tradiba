from tradiba.strategy.analytics.learning import StrategicLearningFramework

def test_learning():
    framework = StrategicLearningFramework()
    res = framework.learn({}, {})
    assert res["accuracy"] == 0.85
