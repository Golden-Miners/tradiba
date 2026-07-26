import uuid
from tradiba.autonomous_research.strategy_generator import StrategyGenerator

def test_strategy_generation():
    generator = StrategyGenerator()
    candidate = generator.generate(uuid.uuid4())
    
    assert candidate.status == "EXPERIMENTAL"
    assert "fvg_formed" in candidate.entry_conditions
