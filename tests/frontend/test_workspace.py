from tradiba.frontend_api.workspace import WorkspaceEngine

def test_workspace_engine():
    engine = WorkspaceEngine()
    
    layout = {"theme": "dark", "panels": ["charts", "signals"]}
    engine.save_layout("user_1", layout)
    
    saved = engine.get_layout("user_1")
    assert saved["theme"] == "dark"
    assert "signals" in saved["panels"]
