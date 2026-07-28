from tradiba.hermes.skills.sdk.base import Skill

class DummySkill(Skill):
    def execute(self, context):
        return {"output": "ok"}

def test_skill_sdk():
    s = DummySkill("s1", "TestSkill", "1.0.0")
    assert not s.validate()
    s.initialize()
    assert s.validate()
    s.register_tool("tool_a")
    s.declare_policy("pol_a")
    assert "tool_a" in s.tools
    assert "pol_a" in s.policies
    res = s.execute({})
    assert res == {"output": "ok"}
    s.shutdown()
    assert not s.validate()
