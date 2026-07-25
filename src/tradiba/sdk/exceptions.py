class PluginError(Exception):
    """Base exception for all plugin-related errors."""
    pass

class PluginLoadError(PluginError):
    """Raised when a plugin fails to load."""
    pass

class PluginValidationError(PluginError):
    """Raised when a plugin's manifest or implementation is invalid."""
    pass

class IncompatibleApiVersionError(PluginLoadError):
    """Raised when a plugin requires an API version that is not supported."""
    pass
