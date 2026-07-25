from tradiba.dev.generator import BoilerplateGenerator

def test_strategy_generation():
    generator = BoilerplateGenerator()
    code = generator.generate_strategy("momentum")
    assert "class MomentumStrategy(Strategy):" in code
    assert "def on_tick(self, ctx: Context, data):" in code

def test_event_generation():
    generator = BoilerplateGenerator()
    code = generator.generate_event("trade")
    assert 'name="trade"' in code
    assert 'fields={"id": str}' in code
