import pytest
import asyncio
from tradiba.hermes.collective.registry.capabilities import CapabilityRegistry

def test_registry_register_and_find():
    registry = CapabilityRegistry()
    registry.register_agent("market_1", {"skills": ["market_analysis"]})
    registry.register_agent("risk_1", {"skills": ["risk_assessment"]})
    
    market_agents = registry.find_agents_by_skill("market_analysis")
    assert "market_1" in market_agents
    assert "risk_1" not in market_agents

def test_registry_health_update():
    registry = CapabilityRegistry()
    registry.register_agent("market_1", {"skills": ["market_analysis"]})
    
    registry.update_health("market_1", "OFFLINE")
    market_agents = registry.find_agents_by_skill("market_analysis")
    assert len(market_agents) == 0 # Should not return offline agents
