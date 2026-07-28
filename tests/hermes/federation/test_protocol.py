from tradiba.hermes.federation.protocol.ihcp import InterHermesProtocol

def test_protocol():
    ihcp = InterHermesProtocol()
    msg = ihcp.sign_message({"data": "test"}, "priv")
    assert ihcp.verify_message(msg, "pub")
