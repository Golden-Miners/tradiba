from tradiba.autonomous.execution.fabric import EnterpriseExecutionFabric
from tradiba.autonomous.missions.models import Mission

def test_execution():
    fabric = EnterpriseExecutionFabric()
    m = Mission("1", "goal", "PLANNED", 3)
    assert fabric.execute(m)
