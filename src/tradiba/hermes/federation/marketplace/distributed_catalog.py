from typing import Dict, Any, List

class DistributedCatalog:
    """
    Decentralized Skill Pack sharing.
    """
    def __init__(self):
        self.catalog: Dict[str, Dict[str, Any]] = {}

    def publish_skill(self, skill_name: str, metadata: Dict[str, Any]) -> None:
        self.catalog[skill_name] = metadata

    def search_skills(self, query: str) -> List[Dict[str, Any]]:
        results = []
        for name, meta in self.catalog.items():
            if query in name:
                results.append(meta)
        return results
