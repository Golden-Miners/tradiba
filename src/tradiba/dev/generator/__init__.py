class BoilerplateGenerator:
    """
    Generates SDK boilerplate to reduce developer friction.
    """
    def generate_strategy(self, name: str) -> str:
        return f"""
from tradiba import Strategy, Context

class {name.capitalize()}Strategy(Strategy):
    def on_tick(self, ctx: Context, data):
        pass
"""

    def generate_event(self, name: str) -> str:
        return f"""
from tradiba.dev.schemas import EventSchema

{name}_schema = EventSchema(
    name="{name}",
    version="1.0",
    fields={{"id": str}}
)
"""
