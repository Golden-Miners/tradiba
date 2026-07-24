from .service import ExecutionService

class ExecutionEngine:
    def __init__(self, service: ExecutionService):
        self.service = service
        
    def process(self, trade_plan):
        return self.service.execute(trade_plan)
