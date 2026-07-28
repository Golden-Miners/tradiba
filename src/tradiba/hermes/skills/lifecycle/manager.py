from typing import Dict, Any, Optional
from tradiba.hermes.skills.sdk.base import Skill

class SkillLifecycleManager:
    """
    Manages Skill installation, activation, upgrade, rollback, deprecation, and removal.
    """
    def __init__(self):
        self.installed_skills: Dict[str, Skill] = {}
        self.active_skills: Dict[str, Skill] = {}
        self.skill_states: Dict[str, str] = {}

    def install(self, skill: Skill) -> bool:
        self.installed_skills[skill.id] = skill
        self.skill_states[skill.id] = "INSTALLED"
        return True

    def activate(self, skill_id: str, config: Optional[Dict[str, Any]] = None) -> bool:
        if skill_id in self.installed_skills:
            skill = self.installed_skills[skill_id]
            skill.initialize(config)
            self.active_skills[skill_id] = skill
            self.skill_states[skill_id] = "ACTIVE"
            return True
        return False

    def upgrade(self, skill_id: str, new_skill: Skill) -> bool:
        if skill_id in self.installed_skills:
            self.deactivate(skill_id)
            self.installed_skills[skill_id] = new_skill
            self.activate(skill_id)
            self.skill_states[skill_id] = "UPGRADED"
            return True
        return False

    def deactivate(self, skill_id: str) -> bool:
        if skill_id in self.active_skills:
            skill = self.active_skills.pop(skill_id)
            skill.shutdown()
            self.skill_states[skill_id] = "INSTALLED"
            return True
        return False

    def remove(self, skill_id: str) -> bool:
        self.deactivate(skill_id)
        if skill_id in self.installed_skills:
            self.installed_skills.pop(skill_id)
            self.skill_states[skill_id] = "REMOVED"
            return True
        return False
