from tradiba.autonomous.missions.models import Mission
from tradiba.autonomous.kernel.os import EnterpriseCognitiveKernel
from tradiba.autonomous.planner.cognitive_planner import CognitiveMissionPlanner

class AutonomousEnterpriseSDK:
    """
    Exposes the developer API for missions, execution, observation, and learning.
    """
    def __init__(self):
        self.kernel = EnterpriseCognitiveKernel()
        self.planner = CognitiveMissionPlanner()

    def create_mission(self, goal: str) -> Mission:
        return self.planner.plan_mission(goal)

    def execute(self, mission: Mission) -> bool:
        return self.kernel.execute_mission(mission.id)
