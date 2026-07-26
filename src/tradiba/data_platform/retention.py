from uuid import UUID

class RetentionManager:
    """Evaluates and executes lifecycle retention rules."""
    def __init__(self) -> None:
        # Maps dataset classification to max age days
        self._policies: dict[str, int] = {
            "tick_data": 5 * 365,
            "order_events": 7 * 365,
            "metrics": 547, # 18 months
            "research": 90
        }
        self._purged: list[UUID] = []

    def set_policy(self, classification: str, max_age_days: int) -> None:
        self._policies[classification] = max_age_days

    def evaluate(self, dataset_id: UUID, classification: str, age_days: int) -> bool:
        """Returns True if the dataset exceeds its retention limit."""
        limit = self._policies.get(classification)
        if limit is None:
            return False
        return age_days > limit
        
    def purge(self, dataset_id: UUID) -> None:
        """Executes the logical deletion of a dataset."""
        if dataset_id not in self._purged:
            self._purged.append(dataset_id)
