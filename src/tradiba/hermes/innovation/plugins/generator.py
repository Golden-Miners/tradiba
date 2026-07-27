from typing import Dict, Any

class PluginGenerator:
    """
    Generates draft plugins compliant with the existing Plugin SDK.
    """
    def __init__(self):
        pass
        
    def generate_plugin(self, name: str) -> Dict[str, Any]:
        return {
            "manifest": {
                "name": name,
                "version": "0.1.0",
                "status": "DRAFT"
            },
            "code": "class MyPlugin:\n    pass\n",
            "tests": "def test_plugin(): pass\n"
        }
