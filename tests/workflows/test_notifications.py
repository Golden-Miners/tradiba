from tradiba.workflows.notifications import NotificationRouter, NotificationDestination

def test_notification_routing():
    router = NotificationRouter()
    
    router.send(NotificationDestination.EMAIL, "info", "test message")
    router.send(NotificationDestination.EMAIL, "critical", "escalate me")
    
    messages = router.get_sent_messages()
    assert len(messages) == 2
    assert messages[0] == (NotificationDestination.EMAIL, "info", "test message")
    assert messages[1] == (NotificationDestination.PAGERDUTY, "critical", "escalate me")
