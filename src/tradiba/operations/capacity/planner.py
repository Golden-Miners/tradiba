from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

class ResourceUsage(BaseModel):
    timestamp: float
    cpu_percent: float
    memory_mb: float
    disk_mb: float
    network_rx_kb: float
    network_tx_kb: float
    kafka_throughput_msg_sec: float
    gpu_utilization_percent: Optional[float] = None

class CapacityForecast(BaseModel):
    service: str
    forecast_date: float
    predicted_cpu_percent: float
    predicted_memory_mb: float
    days_to_exhaustion: Optional[int]
    scaling_recommendation: str

class CapacityPlanner:
    """Forecasts resource usage and plans infrastructure capacity."""

    def __init__(self):
        self.usage_history: Dict[str, List[ResourceUsage]] = {}

    def record_usage(self, service: str, usage: ResourceUsage):
        if service not in self.usage_history:
            self.usage_history[service] = []
        self.usage_history[service].append(usage)
        # Keep only the last 30 days roughly
        if len(self.usage_history[service]) > 43200: # Assuming 1 point per minute
            self.usage_history[service].pop(0)

    def generate_forecast(self, service: str, days_ahead: int = 30) -> CapacityForecast:
        history = self.usage_history.get(service, [])
        if not history:
            return CapacityForecast(
                service=service,
                forecast_date=datetime.utcnow().timestamp() + (days_ahead * 86400),
                predicted_cpu_percent=0.0,
                predicted_memory_mb=0.0,
                days_to_exhaustion=None,
                scaling_recommendation="No data available to generate forecast."
            )

        # Simple linear projection for demonstration
        latest_cpu = history[-1].cpu_percent
        latest_mem = history[-1].memory_mb
        
        # Fake growth trend
        projected_cpu = min(100.0, latest_cpu * 1.1)
        projected_mem = latest_mem * 1.15
        
        exhaustion = None
        recommendation = "Current capacity is sufficient."
        
        if projected_cpu > 80.0 or projected_mem > 16000.0:
            exhaustion = max(1, int((100.0 - latest_cpu) / (projected_cpu - latest_cpu + 0.1)))
            recommendation = f"Recommend vertical scaling or adding {service} replicas within {exhaustion} days."

        return CapacityForecast(
            service=service,
            forecast_date=datetime.utcnow().timestamp() + (days_ahead * 86400),
            predicted_cpu_percent=projected_cpu,
            predicted_memory_mb=projected_mem,
            days_to_exhaustion=exhaustion,
            scaling_recommendation=recommendation
        )
