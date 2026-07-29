from typing import Dict, Any

class QuantEndpoints:
    """
    REST Endpoints for the quant suite.
    """
    def handle_alpha(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "success"}
