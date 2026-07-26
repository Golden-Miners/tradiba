from tradiba.aiops.configuration import PlatformSnapshot
from tradiba.aiops.anomaly import Anomaly

class RootCauseAnalyzer:
    """Infers reasoning chains from observed anomalies."""
    def analyze(self, snapshot: PlatformSnapshot, anomalies: list[Anomaly]) -> list[str]:
        chains = []
        for anomaly in anomalies:
            if anomaly.type == "latency_spike":
                chains.append(
                    "Execution delay\n↓\nBroker latency spike\n↓\nNetwork congestion\n↓\nIncreased slippage"
                )
            elif anomaly.type == "resource_exhaustion":
                chains.append(
                    "Memory exhaustion\n↓\nMemory leak in data loader\n↓\nOOM Kill risk"
                )
            else:
                chains.append(f"Unmapped anomaly: {anomaly.type}")
        return chains
