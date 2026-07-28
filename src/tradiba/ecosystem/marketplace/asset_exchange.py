from typing import Dict, Any, List

class AssetExchange:
    """
    AI Asset Marketplace for sharing models, prompts, agents, and datasets.
    """
    def __init__(self):
        self.assets: Dict[str, Dict[str, Any]] = {}

    def register_asset(self, asset_id: str, metadata: Dict[str, Any]) -> None:
        self.assets[asset_id] = metadata

    def search_assets(self, query: str) -> List[Dict[str, Any]]:
        return [meta for aid, meta in self.assets.items() if query in aid]
