
class StatisticalValidator:
    """
    Significance testing, confidence intervals, effect size estimation.
    """
    def __init__(self):
        self.min_significance = 0.05
        
    def validate(self, p_value: float) -> bool:
        return p_value < self.min_significance
