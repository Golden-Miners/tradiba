import pytest
import asyncio
from tradiba.hermes.collective.blackboard.memory import BlackboardMemory

@pytest.mark.asyncio
async def test_blackboard_operations():
    bb = BlackboardMemory()
    
    await bb.update_market_state({"BTC": 50000})
    state = await bb.get_section("market_state")
    assert state["BTC"] == 50000
    
    await bb.append_research_finding({"title": "Bull run"})
    findings = await bb.get_section("research_findings")
    assert len(findings) == 1
    assert findings[0]["title"] == "Bull run"
