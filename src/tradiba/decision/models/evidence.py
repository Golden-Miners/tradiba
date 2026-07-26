from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass(frozen=True)
class Evidence:
    """Represents an immutable, versioned piece of evidence."""
    evidence_id: UUID
    source: str
    created_at: datetime
    content: str
