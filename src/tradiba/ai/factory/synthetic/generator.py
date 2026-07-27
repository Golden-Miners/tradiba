from typing import Dict, Any, List

class SyntheticDataPlatform:
    """
    Generates and versions datasets for various trading/AI scenarios.
    """
    def __init__(self):
        self.datasets: Dict[str, List[Dict[str, Any]]] = {}
        
    def generate_dataset(self, name: str, scenario: str, size: int) -> str:
        version = f"{name}_v1.0"
        self.datasets[version] = [{"scenario": scenario, "id": i} for i in range(size)]
        return version
        
    def get_dataset(self, version: str) -> List[Dict[str, Any]]:
        return self.datasets.get(version, [])
