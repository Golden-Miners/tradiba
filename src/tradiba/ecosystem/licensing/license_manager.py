from typing import Dict, Any

class LicenseManager:
    """
    License issuance, subscription management, and compliance checks.
    """
    def __init__(self):
        self.licenses: Dict[str, Dict[str, Any]] = {}

    def issue_license(self, tenant_id: str, app_id: str, tier: str) -> str:
        lic_id = f"lic_{tenant_id}_{app_id}"
        self.licenses[lic_id] = {"tier": tier, "active": True}
        return lic_id

    def verify_license(self, lic_id: str) -> bool:
        return self.licenses.get(lic_id, {}).get("active", False)
