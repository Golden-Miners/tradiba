import time

class RecoverableExecutionError(Exception):
    pass

class RetryPolicy:
    max_attempts = 5
    initial_delay = 1
    multiplier = 2

    def execute(self, func, *args, **kwargs):
        delay = self.initial_delay
        last_exception = None
        for attempt in range(self.max_attempts):
            try:
                return func(*args, **kwargs)
            except RecoverableExecutionError as e:
                last_exception = e
                if attempt < self.max_attempts - 1:
                    time.sleep(delay)
                    delay *= self.multiplier
            except Exception as e:
                # Non-recoverable error, raise immediately
                raise e
        raise last_exception
