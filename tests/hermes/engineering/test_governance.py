from tradiba.hermes.engineering.governance.engineering_governance import DevelopmentGovernance

def test_governance():
    gov = DevelopmentGovernance()
    assert gov.can_merge("pr1", {"ci": True, "human": True})
    assert "pr1" in gov.approved_prs
    assert not gov.can_merge("pr2", {"ci": True, "human": False})
