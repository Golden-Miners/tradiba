from dataclasses import dataclass, field

@dataclass(frozen=True)
class CircuitBreakerConfig:
    failure_threshold: int = 5
    recovery_timeout_seconds: float = 60.0

@dataclass(frozen=True)
class RateLimiterConfig:
    max_requests: int = 100
    time_window_seconds: float = 1.0

@dataclass(frozen=True)
class WatchdogConfig:
    heartbeat_timeout_seconds: float = 10.0
    max_missed_heartbeats: int = 3

@dataclass(frozen=True)
class ResilienceConfig:
    circuit_breaker: CircuitBreakerConfig = field(default_factory=CircuitBreakerConfig)
    rate_limiter: RateLimiterConfig = field(default_factory=RateLimiterConfig)
    watchdog: WatchdogConfig = field(default_factory=WatchdogConfig)
