from typing import Dict, Any

class ReproducibilityAuditor:
    """Enforces experiment reproducibility constraints."""
    
    def verify_reproducibility(self, experiment_metadata: Dict[str, Any]) -> bool:
        """
        Ensures that a given experiment run has enough metadata to be exactly reproduced.
        """
        required_keys = {"dataset_version", "software_version", "random_seed"}
        return required_keys.issubset(experiment_metadata.keys())
