class EventStoreError(Exception):
    pass

class ConcurrencyException(EventStoreError):
    pass

class UnknownEventException(EventStoreError):
    pass
