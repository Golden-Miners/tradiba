from abc import ABC, abstractmethod
from tradiba.events.envelope import EventEnvelope

class Projector(ABC):
    """
    Projectors listen to events and update read models.
    """
    
    @abstractmethod
    def project(self, envelope: EventEnvelope) -> None:
        ...
