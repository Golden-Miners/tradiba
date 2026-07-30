from tradiba.modelops.retraining.automator import RetrainingAutomator

def test_retraining():
    ret = RetrainingAutomator()
    assert ret.trigger_retraining("m1")
