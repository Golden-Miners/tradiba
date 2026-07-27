from tradiba.notifications.escalation import EscalationPolicy, EscalationStep

def test_escalation_policy():
    notified = []
    
    def mock_notify(target, data):
        notified.append(target)
        
    # State mock
    ack_state = {"a1": False}
    
    def mock_check_ack(alert_id):
        return ack_state.get(alert_id, False)
        
    policy = EscalationPolicy(
        name="Critical Alert",
        steps=[
            EscalationStep(delay_seconds=0, target_role_or_user="trader"),
            EscalationStep(delay_seconds=0, target_role_or_user="admin")
        ],
        notify_action=mock_notify
    )
    
    # Test full escalation
    policy.execute("a1", {}, mock_check_ack)
    assert len(notified) == 2
    assert notified[0] == "trader"
    assert notified[1] == "admin"
    
    notified.clear()
    
    # Test early acknowledgement
    ack_state["a1"] = True
    policy.execute("a1", {}, mock_check_ack)
    assert len(notified) == 0
