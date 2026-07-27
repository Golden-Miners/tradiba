from typing import Dict, Any, List

class ContextEngine:
    """
    Dynamically assembles and filters contextual data for skills and planners.
    """
    def __init__(self):
        pass
        
    def build_context(self, state: Dict[str, Any], requirements: List[str]) -> Dict[str, Any]:
        """
        Filters the state down to only the requirements specified to minimize overhead.
        """
        filtered_context = {}
        for req in requirements:
            if req in state:
                filtered_context[req] = state[req]
        return filtered_context
