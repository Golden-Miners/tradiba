from tradiba.security.audit.trail import AuditLogger

def test_audit_logging():
    audit = AuditLogger()
    
    audit.log("LOGIN_FAILED", "u1", "auth_service", {"ip": "1.1.1.1"})
    audit.log("TRADE_EXECUTED", "u2", "order_123", {"symbol": "EURUSD"})
    
    assert len(audit.logs) == 2
    
    failed_logins = audit.search(action="LOGIN_FAILED")
    assert len(failed_logins) == 1
    assert failed_logins[0].actor_id == "u1"
