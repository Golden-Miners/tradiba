from tradiba.hermes.innovation.generators.agent_generator import AgentGenerator

def test_agent_generation():
    gen = AgentGenerator()
    agent = gen.generate_agent("Macro Research")
    
    assert agent["name"] == "MacroResearchAgent"
    assert agent["governance_scope"] == "RESEARCH_ONLY"
