from tradiba.ecosystem.marketplace.app_store import AppStore
from tradiba.ecosystem.marketplace.asset_exchange import AssetExchange

def test_marketplace():
    store = AppStore()
    store.publish("app1", {"name": "app1"})
    assert store.install("app1")

    exchange = AssetExchange()
    exchange.register_asset("asset1", {"type": "model"})
    assert len(exchange.search_assets("asset1")) == 1
