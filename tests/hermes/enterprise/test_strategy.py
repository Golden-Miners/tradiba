from tradiba.hermes.enterprise.strategy.planning import StrategicPlanningEngine

def test_strategy():
    engine = StrategicPlanningEngine()
    engine.add_objective("obj1", "Grow")
    assert engine.get_objective("obj1")["title"] == "Grow"
