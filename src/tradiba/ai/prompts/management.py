from typing import Dict, Any

class PromptPlatform:
    """
    Manages prompt templates, versioning, evaluation, and A/B testing.
    """
    def __init__(self):
        self.templates: Dict[str, Dict[str, Any]] = {}
        
    def register_prompt(self, prompt_id: str, template: str, version: str = "1.0"):
        if prompt_id not in self.templates:
            self.templates[prompt_id] = {}
        self.templates[prompt_id][version] = template
        
    def get_prompt(self, prompt_id: str, version: str = "1.0") -> str:
        return self.templates.get(prompt_id, {}).get(version, "")
        
    def render(self, prompt_id: str, variables: Dict[str, Any], version: str = "1.0") -> str:
        template = self.get_prompt(prompt_id, version)
        for k, v in variables.items():
            template = template.replace(f"{{{k}}}", str(v))
        return template
