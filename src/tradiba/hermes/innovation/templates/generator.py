from typing import Dict, Any, List

class PlanningTemplateGenerator:
    """
    Creates reusable planning templates for recurring cognitive tasks.
    """
    def __init__(self):
        pass
        
    def generate_template(self, name: str, observations: List[str]) -> Dict[str, Any]:
        return {
            "template_name": name,
            "steps": observations,
            "benchmark_score": 0.0,
            "status": "DRAFT"
        }
