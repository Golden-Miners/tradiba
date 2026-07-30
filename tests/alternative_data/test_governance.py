from tradiba.alternative_data.governance.workflow import AlternativeDataGovernance

def test_governance():
    gov = AlternativeDataGovernance()
    assert gov.review_dataset("d1")
