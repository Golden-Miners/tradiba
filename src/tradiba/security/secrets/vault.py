from cryptography.fernet import Fernet
import os
import json
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class SecretsManager:
    """Manages encrypted storage and retrieval of sensitive data (API keys, passwords)."""
    
    def __init__(self, key_path: str = "secrets.key", data_path: str = "secrets.enc"):
        self.key_path = key_path
        self.data_path = data_path
        self._key = self._load_or_generate_key()
        self._cipher = Fernet(self._key)
        self._secrets: Dict[str, Any] = self._load_secrets()
        
    def _load_or_generate_key(self) -> bytes:
        if os.path.exists(self.key_path):
            with open(self.key_path, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as f:
                f.write(key)
            return key
            
    def _load_secrets(self) -> Dict[str, Any]:
        if not os.path.exists(self.data_path):
            return {}
        try:
            with open(self.data_path, "rb") as f:
                encrypted_data = f.read()
                if not encrypted_data:
                    return {}
                decrypted = self._cipher.decrypt(encrypted_data)
                return json.loads(decrypted.decode("utf-8"))
        except Exception as e:
            logger.error(f"Failed to load secrets: {e}")
            return {}
            
    def _save_secrets(self):
        try:
            data = json.dumps(self._secrets).encode("utf-8")
            encrypted = self._cipher.encrypt(data)
            with open(self.data_path, "wb") as f:
                f.write(encrypted)
        except Exception as e:
            logger.error(f"Failed to save secrets: {e}")
            
    def set_secret(self, key: str, value: str):
        self._secrets[key] = value
        self._save_secrets()
        
    def get_secret(self, key: str) -> Optional[str]:
        return self._secrets.get(key)
        
    def delete_secret(self, key: str):
        if key in self._secrets:
            del self._secrets[key]
            self._save_secrets()
