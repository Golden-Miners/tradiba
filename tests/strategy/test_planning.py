from tradiba.strategy.planning.engine import StrategicPlanningEngine

def test_planning():
    engine = StrategicPlanningEngine()
    engine.create_plan("p1", {"vision": "AI"})
    assert engine.get_plan("p1")["vision"] == "AI"
