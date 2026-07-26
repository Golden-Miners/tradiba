from dataclasses import dataclass
from tradiba.aiops.configuration import PlatformSnapshot
from tradiba.aiops.summarizer import EventSummarizer
from tradiba.aiops.health import StrategyHealthEngine
from tradiba.aiops.anomaly import AnomalyDetector
from tradiba.aiops.recommendations import RecommendationEngine
from tradiba.aiops.root_cause import RootCauseAnalyzer
from tradiba.aiops.explain import ExplainabilityEngine
from typing import Any

@dataclass
class DailyOperationalSummary:
    summary: str
    strategy_health: dict[str, Any]
    active_anomalies: list[Any]
    recommendations: list[Any]
    explanations: list[Any]

class OperationalInsightsDashboard:
    """Aggregates all AI operations data for the dashboard."""
    
    def __init__(self) -> None:
        self.summarizer = EventSummarizer()
        self.health_engine = StrategyHealthEngine()
        self.anomaly_detector = AnomalyDetector()
        self.recommender = RecommendationEngine()
        self.rca = RootCauseAnalyzer()
        self.explainer = ExplainabilityEngine()

    def generate_dashboard_data(self, snapshot: PlatformSnapshot) -> DailyOperationalSummary:
        summary = self.summarizer.summarize(snapshot.alerts)
        
        health_scores = {}
        for strat in snapshot.strategies:
            strat_id = strat.get("id", "unknown")
            health_scores[strat_id] = self.health_engine.calculate_health(strat)
            
        anomalies = self.anomaly_detector.detect(snapshot)
        recommendations = self.recommender.generate(anomalies)
        reasoning_chains = self.rca.analyze(snapshot, anomalies)
        
        explanations = []
        # Zip assumes 1:1 mapping for anomalies, recommendations, and rca logic in this simplistic implementation
        for anomaly, rec, chain in zip(anomalies, recommendations, reasoning_chains):
            explanations.append(self.explainer.explain(anomaly, rec, chain))
            
        return DailyOperationalSummary(
            summary=summary,
            strategy_health=health_scores,
            active_anomalies=anomalies,
            recommendations=recommendations,
            explanations=explanations
        )
