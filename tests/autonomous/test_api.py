from tradiba.autonomous.api.endpoints import AutonomousEndpoints

def test_api():
    api = AutonomousEndpoints()
    assert api.handle_create_mission({})["status"] == "created"
    assert api.handle_plan({})["status"] == "planned"
