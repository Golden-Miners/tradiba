import logging

logger = logging.getLogger("Licensing")

class LicenseManager:
    """Manages Tradiba Product Licensing."""
    
    def __init__(self):
        self.tier = "Community"
    
    def validate_license(self, license_key: str) -> bool:
        if license_key.startswith("PRO-"):
            self.tier = "Professional"
            return True
        elif license_key.startswith("ENT-"):
            self.tier = "Enterprise"
            return True
        else:
            self.tier = "Community"
            return False
            
    def get_limits(self) -> dict:
        if self.tier == "Enterprise":
            return {"max_users": -1, "max_brokers": -1, "max_strategies": -1}
        elif self.tier == "Professional":
            return {"max_users": 10, "max_brokers": 5, "max_strategies": 20}
        else:
            # Community limits
            return {"max_users": 1, "max_brokers": 1, "max_strategies": 3}
