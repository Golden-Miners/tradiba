from tradiba.hermes.skills.sdk.base import Skill
from tradiba.hermes.skills.lifecycle.manager import SkillLifecycleManager

class DummySkill(Skill):
    def execute(self, context):
        return {}

def test_lifecycle():
    manager = SkillLifecycleManager()
    s1 = DummySkill("s1", "Skill 1", "1.0.0")
    s2 = DummySkill("s1", "Skill 1", "1.1.0")

    assert manager.install(s1)
    assert manager.activate("s1")
    assert manager.skill_states["s1"] == "ACTIVE"

    assert manager.upgrade("s1", s2)
    assert manager.skill_states["s1"] == "UPGRADED"

    assert manager.deactivate("s1")
    assert manager.remove("s1")
    assert manager.skill_states["s1"] == "REMOVED"
