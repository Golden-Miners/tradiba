class DataPlatformError(Exception):
    """Base exception for the Data Platform layer."""
    pass

class SchemaValidationError(DataPlatformError):
    """Raised when data fails schema validation rules."""
    pass

class LineageError(DataPlatformError):
    """Raised when dataset lineage constraints are violated."""
    pass

class RetentionPolicyViolation(DataPlatformError):
    """Raised when an action violates data retention policies."""
    pass
