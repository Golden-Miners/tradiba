from typing import Dict, Any, List, Optional

class SkillMarketplaceCatalog:
    """
    Marketplace catalog with metadata search (domain, tags, popularity, compatibility).
    """
    def __init__(self):
        self.catalog: Dict[str, Dict[str, Any]] = {}

    def publish_skill(self, skill_id: str, metadata: Dict[str, Any]) -> bool:
        self.catalog[skill_id] = metadata
        return True

    def search(self, domain: Optional[str] = None, tag: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        for metadata in self.catalog.values():
            if domain and metadata.get("domain") != domain:
                continue
            if tag and tag not in metadata.get("tags", []):
                continue
            results.append(metadata)
        return results

    def get_metadata(self, skill_id: str) -> Optional[Dict[str, Any]]:
        return self.catalog.get(skill_id)
