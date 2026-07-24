from tradiba.events.bus import EventBus
from .synchronizer import PortfolioSynchronizer
from .repository import PortfolioRepository
from .events import PortfolioUpdatedEvent

class PortfolioService:
    def __init__(
        self,
        sync: PortfolioSynchronizer,
        repository: PortfolioRepository,
        bus: EventBus
    ):
        self.sync = sync
        self.repository = repository
        self.bus = bus

    def synchronize(self):
        portfolio = self.sync.synchronize()
        self.repository.save(portfolio)
        self.bus.publish(
            PortfolioUpdatedEvent(portfolio)
        )
