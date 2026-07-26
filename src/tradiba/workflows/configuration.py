class WorkflowConfiguration:
    """Workflow-specific configuration loader."""
    def __init__(self, config_dict: dict) -> None:
        self._config = config_dict
        
    def get(self, key: str, default: str | None = None) -> str | None:
        return self._config.get(key, default)
