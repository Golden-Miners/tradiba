from tradiba.hermes.platform.planner.engine import UnifiedPlanningEngine

def test_planner():
    engine = UnifiedPlanningEngine()
    engine.create_plan("p1", ["Mission", "Task"])
    assert engine.plans["p1"]["status"] == "DRAFT"
    assert engine.execute_plan("p1")
    assert engine.plans["p1"]["status"] == "EXECUTING"
