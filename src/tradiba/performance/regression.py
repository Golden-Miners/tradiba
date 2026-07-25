from tradiba.performance.report import PerformanceReport
from tradiba.performance.exceptions import RegressionError
import logging

logger = logging.getLogger(__name__)

class PerformanceBaseline:
    """
    Compares new benchmark reports against a stored baseline to detect regressions.
    """
    def __init__(self, baseline_report: PerformanceReport | None = None):
        self.baseline = baseline_report

    def compare(self, current_report: PerformanceReport, allowed_latency_increase_pct: float = 10.0) -> bool:
        """
        Compares the current report against the baseline. Raises RegressionError if outside thresholds.
        """
        if not self.baseline:
            logger.warning("No baseline provided. Assuming baseline established.")
            return True
            
        base_latency = self.baseline.latency_summary.get("avg_ms", 0)
        curr_latency = current_report.latency_summary.get("avg_ms", 0)
        
        if base_latency > 0:
            increase_pct = ((curr_latency - base_latency) / base_latency) * 100.0
            if increase_pct > allowed_latency_increase_pct:
                raise RegressionError(
                    f"Performance regression detected in {current_report.benchmark_name}! "
                    f"Latency increased by {increase_pct:.2f}% (Allowed: {allowed_latency_increase_pct}%)"
                )
                
        logger.info(f"Performance for {current_report.benchmark_name} is within acceptable limits.")
        return True
