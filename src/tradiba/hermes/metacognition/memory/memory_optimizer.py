from typing import Dict, Any, List

class MemoryOptimizer:
    """
    Deduplicates knowledge and compresses context while maintaining provenance.
    """
    def __init__(self):
        pass
        
    def optimize_context(self, context: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen_keys = set()
        optimized = []
        
        for item in reversed(context):
            # Keep newest version of a key
            key = item.get("key")
            if key:
                if key not in seen_keys:
                    seen_keys.add(key)
                    optimized.append(item)
            else:
                optimized.append(item)
                
        return list(reversed(optimized))
