from tradiba.modelops.governance.lifecycle import LifecycleGovernance

def test_governance():
    gov = LifecycleGovernance()
    assert gov.review_promotion("m1")
