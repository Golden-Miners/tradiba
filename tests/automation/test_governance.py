from tradiba.automation.governance.automation_policy import AutomationGovernance

def test_governance():
    gov = AutomationGovernance()
    assert gov.validate_workflow("w1")
    assert gov.check_permissions("u1", "a1")
