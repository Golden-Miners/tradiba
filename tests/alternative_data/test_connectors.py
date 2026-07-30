from tradiba.alternative_data.connectors.sdk import DataConnectorSDK

def test_connectors():
    sdk = DataConnectorSDK()
    assert sdk.connect("c1")
