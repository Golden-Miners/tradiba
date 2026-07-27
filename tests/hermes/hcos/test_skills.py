import pytest
from tradiba.hermes.hcos.skills.framework import CognitiveSkillsFramework, CognitiveSkill

class MockSkill(CognitiveSkill):
    def execute(self, inputs):
        return {"res": "ok"}

def test_skills_framework():
    fw = CognitiveSkillsFramework()
    fw.register_skill(MockSkill("test_skill", ["read"]))
    
    sk = fw.get_skill("test_skill")
    assert sk.name == "test_skill"
    assert fw.list_skills() == ["test_skill"]
    
    with pytest.raises(ValueError):
        fw.get_skill("missing")
