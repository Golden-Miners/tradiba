from typing import List

class JurisdictionPacks:
    """
    Installable rulesets for different regimes (e.g., US, EU).
    """
    def get_rules_for_jurisdiction(self, jurisdiction: str) -> List[str]:
        return [f"rule_1_{jurisdiction}"]
