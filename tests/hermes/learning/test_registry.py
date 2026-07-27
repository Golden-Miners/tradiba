import pytest
import os
from tradiba.hermes.learning.prompts.registry import PromptRegistry

@pytest.fixture
def registry():
    db_path = "test_prompts.db"
    r = PromptRegistry(db_path)
    r.clear_db()
    yield r
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except PermissionError:
            pass

def test_register_and_get_prompt(registry):
    v1 = registry.register_prompt("market_analyzer", "You are an analyzer", {"temp": 0.5})
    assert v1 == 1
    
    v2 = registry.register_prompt("market_analyzer", "You are a better analyzer", {"temp": 0.7})
    assert v2 == 2
    
    latest = registry.get_prompt("market_analyzer")
    assert latest["version"] == 2
    
    old = registry.get_prompt("market_analyzer", version=1)
    assert old["version"] == 1

def test_rollback_prompt(registry):
    registry.register_prompt("risk_eval", "v1", {})
    registry.register_prompt("risk_eval", "v2", {})
    
    registry.rollback_prompt("risk_eval", target_version=1)
    
    latest = registry.get_prompt("risk_eval")
    assert latest["status"] == "ROLLED_BACK"
