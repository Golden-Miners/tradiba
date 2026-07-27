from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class HermesEvent:
    event_type: str
    timestamp: float
    payload: Dict[str, Any]

@dataclass
class HermesGoalCreatedEvent(HermesEvent):
    def __init__(self, timestamp: float, payload: Dict[str, Any]):
        super().__init__("HermesGoalCreated", timestamp, payload)

@dataclass
class HermesPlanGeneratedEvent(HermesEvent):
    def __init__(self, timestamp: float, payload: Dict[str, Any]):
        super().__init__("HermesPlanGenerated", timestamp, payload)

@dataclass
class HermesRecommendationCreatedEvent(HermesEvent):
    def __init__(self, timestamp: float, payload: Dict[str, Any]):
        super().__init__("HermesRecommendationCreated", timestamp, payload)

@dataclass
class HermesReflectionCompletedEvent(HermesEvent):
    def __init__(self, timestamp: float, payload: Dict[str, Any]):
        super().__init__("HermesReflectionCompleted", timestamp, payload)
