class MigrationFailedError(Exception):
    pass

class IncompatibleVersionError(Exception):
    pass

class RollbackFailedError(Exception):
    pass
