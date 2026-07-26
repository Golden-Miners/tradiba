import pytest
from tradiba.agents.orchestrator import AgentOrchestrator
from tradiba.agents.market.agent import MarketIntelligenceAgent
from tradiba.agents.base.context import AgentContext

@pytest.mark.asyncio
async def test_orchestrator_dispatch():
    """Verify orchestrator correctly routes and wraps agent output into a Recommendation."""
    agents = {"market": MarketIntelligenceAgent()}
    orchestrator = AgentOrchestrator(agents)
    
    ctx = AgentContext({}, {}, {}, {}, {}, None, None)
    
    rec = await orchestrator.dispatch("market", ctx)
    assert rec.category == "market_intelligence"
    assert rec.recommended_action == "INCREASE_EXPOSURE"
    assert rec.confidence == 0.85
