from abc import ABC, abstractmethod

class BrokerExecutor(ABC):
    @abstractmethod
    def submit(self, trade_plan):
        pass

    @abstractmethod
    def modify(self, order):
        pass

    @abstractmethod
    def cancel(self, order_id):
        pass

    @abstractmethod
    def synchronize(self):
        pass
