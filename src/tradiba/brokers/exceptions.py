class BrokerError(Exception):
    """Base exception for all broker-related errors."""
    pass

class RoutingError(BrokerError):
    """Raised when the order router cannot find a suitable broker."""
    pass

class CapabilityMismatchError(BrokerError):
    """Raised when a broker lacks the capabilities to execute a signal."""
    pass

class BrokerConnectionError(BrokerError):
    """Raised when unable to connect to a broker."""
    pass
