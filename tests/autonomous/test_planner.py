from tradiba.autonomous.planner.cognitive_planner import CognitiveMissionPlanner

def test_planner():
    planner = CognitiveMissionPlanner()
    m = planner.plan_mission("goal")
    assert m.status == "PLANNED"
