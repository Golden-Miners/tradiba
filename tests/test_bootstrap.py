from tradiba.bootstrap import bootstrap
from tradiba.core.application import Application
from tradiba.core.container import Container
from tradiba.events import EventBus
from tradiba.market.service import MarketDataService

def test_bootstrap():
    app = bootstrap()
    assert isinstance(app, Application)
    
    container = app.container
    assert isinstance(container, Container)
    
    # Verify core components are resolved
    event_bus = container.resolve(EventBus)
    assert isinstance(event_bus, EventBus)
    
    market_data = container.resolve(MarketDataService)
    assert isinstance(market_data, MarketDataService)
    
    # Start and stop to verify lifecycle
    app.start()
    app.stop()
