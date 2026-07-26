from typing import Generic, TypeVar, Any

T = TypeVar('T')
E = TypeVar('E')

class Result(Generic[T, E]):
    """Standard Result type for operations."""
    def __init__(self, is_success: bool, value: T | None = None, error: E | None = None):
        if is_success and error is not None:
            raise ValueError("Success result cannot have an error")
        if not is_success and error is None:
            raise ValueError("Failure result must have an error")
            
        self.is_success = is_success
        self.value = value
        self.error = error

    @classmethod
    def ok(cls, value: T) -> 'Result[T, Any]':
        return cls(is_success=True, value=value)

    @classmethod
    def fail(cls, error: E) -> 'Result[Any, E]':
        return cls(is_success=False, error=error)
