from tradiba.ai.sdk.developer import AIDeveloperSDK

def test_sdk():
    sdk = AIDeveloperSDK()
    assert sdk.register_agent("test", {})
    assert sdk.register_tool("tool", {})
