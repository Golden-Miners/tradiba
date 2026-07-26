from tradiba.frontend_api.portfolio import PortfolioDashboardService

def test_portfolio_dashboard_service():
    service = PortfolioDashboardService()
    
    summary = service.get_summary("tenant_1")
    assert summary["equity"] > 0
    assert "allocations" in summary
