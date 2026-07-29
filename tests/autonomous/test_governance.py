from tradiba.autonomous.governance.framework import HumanGovernanceFramework
from tradiba.autonomous.missions.models import Mission

def test_governance():
    gov = HumanGovernanceFramework()
    m = Mission("1", "g", "NEW", 3)
    assert gov.approve(m)
