from tradiba.hermes.world.model.world import WorldModelBuilder
from tradiba.hermes.world.predictions.framework import PredictionFramework
from tradiba.hermes.world.scenarios.simulator import ScenarioSimulator
from tradiba.hermes.world.optimization.optimizer import PlanOptimizer
from tradiba.hermes.world.planner.adaptive import AdaptivePlanningEngine

def test_adaptive_planner():
    builder = WorldModelBuilder()
    predictor = PredictionFramework()
    simulator = ScenarioSimulator()
    optimizer = PlanOptimizer()
    
    planner = AdaptivePlanningEngine(builder, predictor, simulator, optimizer)
    
    plan = planner.generate_plan({"id": "goal_1"})
    
    assert plan is not None
    assert "id" in plan
    assert "action" in plan
