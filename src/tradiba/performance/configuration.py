from dataclasses import dataclass, field

@dataclass(frozen=True)
class ProfilerConfig:
    enabled: bool = True
    sample_rate: float = 1.0  # 1.0 = 100% of events, 0.1 = 10%

@dataclass(frozen=True)
class BenchmarkConfig:
    iterations: int = 10
    warmup_iterations: int = 2

@dataclass(frozen=True)
class CapacityConfig:
    target_throughput_tps: int = 1000
    max_latency_ms: float = 50.0

@dataclass(frozen=True)
class PerformanceConfig:
    profiler: ProfilerConfig = field(default_factory=ProfilerConfig)
    benchmark: BenchmarkConfig = field(default_factory=BenchmarkConfig)
    capacity: CapacityConfig = field(default_factory=CapacityConfig)
