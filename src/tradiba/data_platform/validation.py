from typing import Any
from tradiba.data_platform.exceptions import SchemaValidationError

class DataQualityValidator:
    """Validates datasets against quality rules."""
    
    def validate_schema(self, data: list[dict[str, Any]], expected_keys: set[str]) -> bool:
        if not data:
            return True
        for row in data:
            if not expected_keys.issubset(row.keys()):
                raise SchemaValidationError(f"Row missing required keys: {expected_keys - row.keys()}")
        return True
        
    def generate_quality_report(self, data: list[dict[str, Any]]) -> dict[str, Any]:
        """Generates a quality score based on missing values and schema consistency."""
        if not data:
            return {"score": 1.0, "issues": []}
            
        issues = []
        total_fields = 0
        missing_fields = 0
        
        for row in data:
            total_fields += len(row)
            missing_fields += sum(1 for v in row.values() if v is None)
            
        score = 1.0 - (missing_fields / total_fields) if total_fields > 0 else 1.0
        
        if score < 1.0:
            issues.append(f"{missing_fields} missing values detected.")
            
        return {"score": score, "issues": issues}
