from .aggregate import Portfolio

class PortfolioSynchronizer:
    def synchronize(self) -> Portfolio:
        raise NotImplementedError
