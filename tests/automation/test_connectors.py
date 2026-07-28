from tradiba.automation.connectors.integration_hub import IntegrationHub

def test_connectors():
    hub = IntegrationHub()
    hub.install_connector("c1", {})
    assert hub.execute_connector("c1", {})
    assert not hub.execute_connector("c2", {})
