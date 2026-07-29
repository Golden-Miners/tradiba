from tradiba.autonomous.missions.models import Mission

def test_missions():
    mission = Mission(id="1", goal="test", status="NEW", autonomy_level=5)
    assert mission.goal == "test"
