
class CodeGenerator:
    """
    Generates domain models, services, and event handlers.
    """
    def __init__(self):
        self.templates = {"service": "class {name}Service:"}
        
    def generate(self, component_type: str, name: str) -> str:
        if component_type in self.templates:
            return self.templates[component_type].format(name=name)
        return ""
