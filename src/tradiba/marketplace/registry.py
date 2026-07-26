from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class StrategyPackage:
    id: str
    version: str
    author: str
    signature: str
    manifest: Dict[str, Any]
    binary_url: Optional[str] = None

class MarketplaceRegistry:
    """
    Reference Implementation: Strategy Marketplace Registry.
    Manages versioned, signed strategy packages for internal deployment.
    """
    
    def __init__(self):
        self._packages: Dict[str, Dict[str, StrategyPackage]] = {}
        
    def publish(self, package: StrategyPackage) -> bool:
        """Publish a new strategy or version."""
        if not self._verify_signature(package):
            raise ValueError("Invalid package signature.")
            
        if package.id not in self._packages:
            self._packages[package.id] = {}
            
        if package.version in self._packages[package.id]:
            raise ValueError(f"Version {package.version} already exists for {package.id}")
            
        self._packages[package.id][package.version] = package
        return True
        
    def _verify_signature(self, package: StrategyPackage) -> bool:
        """Mock signature verification."""
        return len(package.signature) > 10
        
    def get_latest(self, strategy_id: str) -> Optional[StrategyPackage]:
        """Retrieve the latest version of a strategy."""
        versions = self._packages.get(strategy_id, {})
        if not versions:
            return None
        # In reality, parse semver. For mock, just sort strings.
        latest_ver = sorted(versions.keys())[-1]
        return versions[latest_ver]
