from typing import Dict, Any

class InterHermesProtocol:
    """
    Inter-Hermes Communication Protocol (IHCP).
    """
    def sign_message(self, message: Dict[str, Any], private_key: str) -> Dict[str, Any]:
        message["signature"] = "signed_with_" + private_key
        return message

    def verify_message(self, message: Dict[str, Any], public_key: str) -> bool:
        return "signature" in message
