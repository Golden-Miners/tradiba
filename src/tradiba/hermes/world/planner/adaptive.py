from typing import Dict, Any

from tradiba.hermes.world.model.world import WorldModelBuilder
from tradiba.hermes.world.predictions.framework import PredictionFramework
from tradiba.hermes.world.scenarios.simulator import ScenarioSimulator
from tradiba.hermes.world.optimization.optimizer import PlanOptimizer

class AdaptivePlanningEngine:
    """
    Generates and optimizes plans based on the current WorldState and future predictions.
    """
    def __init__(
        self,
        world_builder: WorldModelBuilder,
        predictor: PredictionFramework,
        simulator: ScenarioSimulator,
        optimizer: PlanOptimizer
    ):
        self.world = world_builder
        self.predictor = predictor
        self.simulator = simulator
        self.optimizer = optimizer
        
    def generate_plan(self, goal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Current State -> Predict Future -> Generate Options -> Evaluate Risk -> Rank Plans -> Recommend
        """
        current_state = self.world.get_state()
        
        # Predict future
        _regime = self.predictor.predict_regime(current_state)
        
        # Generate Options
        options = [
            {"id": "plan_A", "action": "scale_up", "risk_score": 0.6, "capital_efficiency": 0.8},
            {"id": "plan_B", "action": "hedge", "risk_score": 0.2, "capital_efficiency": 0.4}
        ]
        
        # Evaluate Risk via Simulation
        for opt in options:
            if opt["action"] == "scale_up":
                _sim_state = self.simulator.run_scenario(current_state, "bear")
                # Adjust risk_score based on simulation
                current_risk = float(opt.get("risk_score", 0.0))
                opt["risk_score"] = min(1.0, current_risk * 1.5)
                
        # Rank Plans
        ranked_plans = self.optimizer.optimize(options)
        
        # Recommend best
        return ranked_plans[0] if ranked_plans else {}
