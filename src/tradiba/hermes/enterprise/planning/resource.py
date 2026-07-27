
class ResourcePlanner:
    """
    Forecasts engineering capacity and compute utilization.
    """
    def __init__(self):
        self.capacity = {"engineering": 100, "compute": 1000}
        
    def forecast(self, metric: str) -> float:
        return self.capacity.get(metric, 0.0)
