from tradiba.automation.approvals.hitl import HumanInTheLoop

def test_approvals():
    hitl = HumanInTheLoop()
    hitl.request_approval("r1", {})
    assert hitl.grant_approval("r1")
    assert not hitl.grant_approval("r2")
