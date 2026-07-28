from tradiba.hermes.skills.sdk.base import Skill
from tradiba.hermes.skills.runtime.execution import SkillExecutionRuntime

class DummySkill(Skill):
    def execute(self, context):
        if context.get("fail"):
            raise ValueError("Execution error")
        return {"result": "success"}

def test_runtime_success():
    s = DummySkill("s1", "TestSkill", "1.0.0")
    s.initialize()
    runtime = SkillExecutionRuntime()
    res = runtime.run(s, {})
    assert res["status"] == "SUCCESS"
    assert res["result"] == {"result": "success"}

def test_runtime_failure():
    s = DummySkill("s1", "TestSkill", "1.0.0")
    s.initialize()
    runtime = SkillExecutionRuntime(max_retries=1)
    res = runtime.run(s, {"fail": True})
    assert res["status"] == "FAILED"
    assert "Execution error" in res["reason"]
