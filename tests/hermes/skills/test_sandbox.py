from tradiba.hermes.skills.sandbox.isolation import SkillSandboxIsolation

def test_sandbox():
    sandbox = SkillSandboxIsolation()
    sandbox.grant_permissions("s1", ["read_market_data", "execute_paper_trade"])

    assert sandbox.check_permission("s1", "read_market_data")
    assert sandbox.check_permission("s1", "execute_paper_trade")
    assert not sandbox.check_permission("s1", "execute_live_trade")
