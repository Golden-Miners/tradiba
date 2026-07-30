import time
from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class SLIMetric(BaseModel):
    service: str
    metric_type: str  # e.g., 'latency', 'availability', 'success_rate'
    value: float
    timestamp: float = Field(default_factory=time.time)

class SLOObjective(BaseModel):
    id: str
    service: str
    description: str
    metric_type: str
    target_value: float
    operator: str # e.g., '>=', '<='
    window_seconds: int = 2592000  # 30 days default

class SLOStatus(BaseModel):
    slo_id: str
    current_value: float
    error_budget_remaining: float
    is_violating: bool
    last_updated: float = Field(default_factory=time.time)

class SLOEngine:
    """Manages Service Level Objectives and Error Budgets for the enterprise."""
    
    def __init__(self):
        self.objectives: Dict[str, SLOObjective] = {}
        self.slis: List[SLIMetric] = []
        self.statuses: Dict[str, SLOStatus] = {}

    def register_slo(self, slo_id: str, service: str, description: str, metric_type: str, target: float, operator: str) -> SLOObjective:
        slo = SLOObjective(
            id=slo_id,
            service=service,
            description=description,
            metric_type=metric_type,
            target_value=target,
            operator=operator
        )
        self.objectives[slo_id] = slo
        # Initialize status
        self.statuses[slo_id] = SLOStatus(
            slo_id=slo_id,
            current_value=100.0 if operator == '>=' else 0.0,
            error_budget_remaining=100.0,
            is_violating=False
        )
        return slo

    def record_sli(self, service: str, metric_type: str, value: float):
        sli = SLIMetric(service=service, metric_type=metric_type, value=value)
        self.slis.append(sli)
        self._evaluate_slos(service, metric_type)

    def _evaluate_slos(self, service: str, metric_type: str):
        for slo in self.objectives.values():
            if slo.service == service and slo.metric_type == metric_type:
                relevant_slis = [s for s in self.slis if s.service == service and s.metric_type == metric_type]
                if not relevant_slis:
                    continue
                
                # Use moving average
                avg_value = sum(s.value for s in relevant_slis) / len(relevant_slis)
                
                is_violating = False
                if slo.operator == '>=' and avg_value < slo.target_value:
                    is_violating = True
                elif slo.operator == '<=' and avg_value > slo.target_value:
                    is_violating = True

                # Deduct error budget simple mock
                error_budget = self.statuses[slo.id].error_budget_remaining
                if is_violating:
                    error_budget -= 1.0 # arbitrary deduction
                
                self.statuses[slo.id] = SLOStatus(
                    slo_id=slo.id,
                    current_value=avg_value,
                    error_budget_remaining=max(0.0, error_budget),
                    is_violating=is_violating
                )

    def get_slo_status(self, slo_id: str) -> Optional[SLOStatus]:
        return self.statuses.get(slo_id)

    def get_all_statuses(self) -> List[SLOStatus]:
        return list(self.statuses.values())
