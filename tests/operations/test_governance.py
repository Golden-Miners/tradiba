from tradiba.operations.governance.ops_policy import OperationsGovernance

def test_governance():
    gov = OperationsGovernance()
    assert gov.evaluate_action("a1", "high") == "Assisted"
    assert gov.evaluate_action("a1", "low") == "Autonomous"
