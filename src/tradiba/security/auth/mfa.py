import pyotp

class MfaService:
    """Handles Time-Based One-Time Password (TOTP) logic."""
    
    @staticmethod
    def generate_secret() -> str:
        """Generates a new base32 secret for MFA setup."""
        return pyotp.random_base32()
        
    @staticmethod
    def get_provisioning_uri(secret: str, email: str, issuer_name: str = "Tradiba") -> str:
        """Generates the provisioning URI to be embedded in a QR code."""
        return pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name=issuer_name)
        
    @staticmethod
    def verify_totp(secret: str, code: str) -> bool:
        """Verifies a given TOTP code against the secret."""
        totp = pyotp.TOTP(secret)
        return totp.verify(code)
