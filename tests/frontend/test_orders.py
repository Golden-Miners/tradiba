from tradiba.frontend_api.orders import OrderTicketService

def test_order_ticket_service():
    service = OrderTicketService()
    
    valid_order = {"asset": "BTC/USD", "size": 1.0, "risk_percentage": 5.0}
    response = service.submit_order(valid_order)
    assert response["status"] == "submitted"
    
    invalid_order = {"asset": "BTC/USD", "size": 5.0, "risk_percentage": 15.0}
    response2 = service.submit_order(invalid_order)
    assert response2["status"] == "rejected"
    assert response2["reason"] == "risk_limit_exceeded"
