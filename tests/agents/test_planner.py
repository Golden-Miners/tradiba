import pytest
from tradiba.agents.orchestrator import AgentOrchestrator
from tradiba.agents.planner import Planner
from tradiba.agents.market.agent import MarketIntelligenceAgent
from tradiba.agents.risk.agent import RiskAdvisorAgent
from tradiba.agents.base.context import AgentContext

@pytest.mark.asyncio
async def test_planner_workflow():
    agents = {
        "market": MarketIntelligenceAgent(),
        "risk": RiskAdvisorAgent()
    }
    orchestrator = AgentOrchestrator(agents)
    planner = Planner(orchestrator)
    
    ctx = AgentContext({}, {}, {}, {}, {}, None, None)
    recs = await planner.run_workflow(["market", "risk"], ctx)
    
    assert len(recs) == 2
    assert recs[0].category == "market_intelligence"
    assert recs[1].category == "risk_advisor"
