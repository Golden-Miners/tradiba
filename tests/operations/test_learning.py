from tradiba.operations.analytics.operational_learning import OperationalLearning

def test_learning():
    learn = OperationalLearning()
    pm = learn.generate_postmortem("i1")
    assert pm["incident"] == "i1"
    assert len(learn.postmortems) == 1
