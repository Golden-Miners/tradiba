from tradiba.data_mesh.marketplace.discovery import MarketplaceDiscovery

def test_marketplace():
    mkt = MarketplaceDiscovery()
    assert mkt.search("query") == []
