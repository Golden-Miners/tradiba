from typing import Dict, Any, List

class FederatedLearning:
    """
    Model exchange and evaluation sharing.
    """
    def __init__(self):
        self.shared_models: Dict[str, Dict[str, Any]] = {}

    def exchange_model(self, model_id: str, metadata: Dict[str, Any]) -> None:
        self.shared_models[model_id] = metadata

    def get_shared_models(self) -> List[Dict[str, Any]]:
        return list(self.shared_models.values())
