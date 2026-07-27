from typing import Dict, Any

class SkillMarketplace:
    """
    Allows capabilities to be packaged as reusable skills.
    """
    def __init__(self):
        self.skills = {}
        
    def install(self, skill_name: str, package: Dict[str, Any]):
        self.skills[skill_name] = package
        
    def get_skill(self, skill_name: str) -> Dict[str, Any]:
        return self.skills.get(skill_name, {})
