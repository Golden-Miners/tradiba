from dataclasses import dataclass

@dataclass
class TwinHealth:
    sync_lag_ms: int
    replay_success_rate: float
    validation_failures: int

class HealthMonitor:
    """Monitors the operational health of the digital twin."""
    
    def check_health(self) -> TwinHealth:
        # Mock health check
        return TwinHealth(
            sync_lag_ms=120,
            replay_success_rate=0.99,
            validation_failures=0
        )
