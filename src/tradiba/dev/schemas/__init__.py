from dataclasses import dataclass, field

@dataclass
class EventSchema:
    """
    Defines the schema for a registered event type.
    """
    name: str
    version: str
    fields: dict[str, type] = field(default_factory=dict)
    compatibility: list[str] = field(default_factory=list)
