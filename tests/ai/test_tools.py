from tradiba.ai.tools.registry import ToolRegistry

def test_tools():
    reg = ToolRegistry()
    reg.register_tool("market_data", {"type": "query"}, ["data:read"])
    assert "data:read" in reg.get_tool("market_data")["permissions"]
