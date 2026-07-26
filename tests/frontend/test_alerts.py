from tradiba.frontend_api.alerts import AlertCenterService

def test_alert_center_service():
    service = AlertCenterService()
    
    service.push_alert({"msg": "Test Alert", "severity": "HIGH"})
    service.push_alert({"msg": "Info Alert", "severity": "INFO"})
    
    high_alerts = service.get_alerts("HIGH")
    assert len(high_alerts) == 1
    assert high_alerts[0]["severity"] == "HIGH"
    
    all_alerts = service.get_alerts()
    assert len(all_alerts) == 2
