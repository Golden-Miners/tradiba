from tradiba.compliance.aml.integration import AMLIntegration

def test_aml():
    aml = AMLIntegration()
    assert aml.check_customer("c1")
