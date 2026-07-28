from tradiba.hermes.skills.telemetry.metrics import SkillObservabilityTracker
from tradiba.hermes.skills.templates.toolkit import SkillDevelopmentToolkit

def test_telemetry():
    tracker = SkillObservabilityTracker()
    tracker.record_execution("s1", success=True, latency_ms=45.2, tokens_used=150)
    tracker.record_execution("s1", success=False, latency_ms=12.0, tokens_used=50)

    m = tracker.get_metrics("s1")
    assert m["total_executions"] == 2
    assert m["successes"] == 1
    assert m["failures"] == 1
    assert m["tokens_used"] == 200

def test_toolkit():
    toolkit = SkillDevelopmentToolkit()
    scaffold = toolkit.scaffold_skill("my_skill", "My Skill", "trading")
    assert scaffold["id"] == "my_skill"

    pkg = toolkit.package_skill("my_skill")
    assert pkg["signed"]
