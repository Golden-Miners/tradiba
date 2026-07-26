from abc import ABC, abstractmethod

class SecretProvider(ABC):
    """Abstract interface for managing secrets across the fleet."""
    
    @abstractmethod
    def get_secret(self, logical_name: str) -> str | None:
        pass
        
    @abstractmethod
    def rotate_secret(self, logical_name: str, new_value: str) -> None:
        pass
        
    @abstractmethod
    def revoke_secret(self, logical_name: str) -> None:
        pass

class LocalEncryptedStore(SecretProvider):
    """In-memory stub for testing."""
    def __init__(self) -> None:
        self._secrets: dict[str, str] = {}
        
    def get_secret(self, logical_name: str) -> str | None:
        return self._secrets.get(logical_name)
        
    def rotate_secret(self, logical_name: str, new_value: str) -> None:
        self._secrets[logical_name] = new_value
        
    def revoke_secret(self, logical_name: str) -> None:
        if logical_name in self._secrets:
            del self._secrets[logical_name]
