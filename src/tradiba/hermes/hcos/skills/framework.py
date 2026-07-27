from typing import Dict, Any, List

class CognitiveSkill:
    def __init__(self, name: str, required_permissions: List[str]):
        self.name = name
        self.required_permissions = required_permissions
        
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Skill must implement execute()")

class CognitiveSkillsFramework:
    """
    Manages pluggable skills.
    """
    def __init__(self):
        self.registry: Dict[str, CognitiveSkill] = {}
        
    def register_skill(self, skill: CognitiveSkill):
        self.registry[skill.name] = skill
        
    def get_skill(self, name: str) -> CognitiveSkill:
        if name not in self.registry:
            raise ValueError(f"Skill {name} not found.")
        return self.registry[name]
        
    def list_skills(self) -> List[str]:
        return list(self.registry.keys())
