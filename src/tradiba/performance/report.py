from dataclasses import dataclass, field
from typing import Any

@dataclass(slots=True)
class PerformanceReport:
    """
    Summarizes the results of a benchmark run.
    """
    benchmark_name: str
    latency_summary: dict[str, float] = field(default_factory=dict)
    memory_summary: dict[str, float] = field(default_factory=dict)
    cpu_summary: dict[str, float] = field(default_factory=dict)
    bottlenecks: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
