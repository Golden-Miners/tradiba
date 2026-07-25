from typing import Callable, Any

def on(event_name: str) -> Callable[..., Any]:
    """
    Decorator to subscribe a strategy method to a specific platform event.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        # Tag the function so the runtime can discover it
        if not hasattr(func, "_subscriptions"):
            func._subscriptions = [] # type: ignore
        func._subscriptions.append(event_name) # type: ignore
        return func
    return decorator
