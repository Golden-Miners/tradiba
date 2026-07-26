from tradiba.frontend_api.insights import AIInsightService

def test_ai_insight_service():
    service = AIInsightService()
    
    insights = service.get_insights()
    assert len(insights) > 0
    assert "narrative" in insights[0]
    assert "evidence_link" in insights[0]
