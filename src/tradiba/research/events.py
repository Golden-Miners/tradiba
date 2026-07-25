from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class PredictionGeneratedEvent:
    model_id: UUID
    timestamp: datetime
    features: dict
    prediction: float | str | dict
    confidence: float

@dataclass(frozen=True)
class RegimeChangedEvent:
    timestamp: datetime
    old_regime: str
    new_regime: str
    confidence: float

@dataclass(frozen=True)
class ModelLoadedEvent:
    model_id: UUID
    timestamp: datetime
    mode: str # 'shadow' or 'production'

@dataclass(frozen=True)
class ModelPromotedEvent:
    model_id: UUID
    timestamp: datetime
    promoted_by: str
