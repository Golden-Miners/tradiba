from typing import Any, TypeVar, Generic

T = TypeVar('T')

class Parameter(Generic[T]):
    """Base class for declarative strategy parameters using Python descriptors."""
    def __init__(self, default: T, name: str | None = None) -> None:
        self.default = default
        self.name = name
        self._values: dict[Any, T] = {}

    def __set_name__(self, owner: Any, name: str) -> None:
        self.name = name

    def __get__(self, instance: Any, owner: Any) -> Any:
        if instance is None:
            return self
        return self._values.get(instance, self.default)

    def __set__(self, instance: Any, value: T) -> None:
        self.validate(value)
        self._values[instance] = value
        
    def validate(self, value: T) -> None:
        pass

class FloatParameter(Parameter[float]):
    def __init__(self, default: float, minimum: float | None = None, maximum: float | None = None) -> None:
        super().__init__(default)
        self.minimum = minimum
        self.maximum = maximum
        
    def validate(self, value: float) -> None:
        if self.minimum is not None and value < self.minimum:
            raise ValueError(f"Value {value} below minimum {self.minimum}")
        if self.maximum is not None and value > self.maximum:
            raise ValueError(f"Value {value} above maximum {self.maximum}")

class IntParameter(Parameter[int]):
    def __init__(self, default: int, minimum: int | None = None, maximum: int | None = None) -> None:
        super().__init__(default)
        self.minimum = minimum
        self.maximum = maximum
        
    def validate(self, value: int) -> None:
        if self.minimum is not None and value < self.minimum:
            raise ValueError(f"Value {value} below minimum {self.minimum}")
        if self.maximum is not None and value > self.maximum:
            raise ValueError(f"Value {value} above maximum {self.maximum}")
