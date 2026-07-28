from typing import Dict

class BillingMeter:
    """
    Tracking usage and calculating billing/revenue data.
    """
    def __init__(self):
        self.usage: Dict[str, int] = {}

    def record_usage(self, tenant_id: str, app_id: str, units: int) -> None:
        key = f"{tenant_id}:{app_id}"
        self.usage[key] = self.usage.get(key, 0) + units

    def get_bill(self, tenant_id: str, app_id: str) -> float:
        key = f"{tenant_id}:{app_id}"
        return self.usage.get(key, 0) * 0.05  # $0.05 per unit
