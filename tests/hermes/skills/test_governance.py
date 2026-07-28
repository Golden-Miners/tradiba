from tradiba.hermes.skills.sandbox.isolation import SkillSandboxIsolation
from tradiba.hermes.skills.governance.skill_governance import SkillGovernanceEngine

def test_governance():
    sandbox = SkillSandboxIsolation()
    sandbox.grant_permissions("s1", ["read_data"])
    gov = SkillGovernanceEngine(sandbox)

    assert gov.validate_request("s1", ["read_data"])
    assert not gov.validate_request("s1", ["write_data"])
    assert len(gov.audit_logs) == 2
