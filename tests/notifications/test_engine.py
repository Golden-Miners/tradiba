from tradiba.notifications.models.notification import Notification, NotificationSeverity, DeliveryStatus
from tradiba.notifications.engine import NotificationEngine
from tradiba.notifications.preferences import PreferencesService
from tradiba.notifications.email import EmailDispatcher

def test_engine_dispatching():
    prefs = PreferencesService()
    email_dispatch = EmailDispatcher()
    
    engine = NotificationEngine(prefs, [email_dispatch])
    
    notification = Notification(
        id="n1",
        type="alert",
        severity=NotificationSeverity.INFO,
        recipient_id="u1",
        title="Test",
        message="Message"
    )
    
    result = engine.dispatch_notification(notification, {"email": "test@test.com"})
    
    assert result.status == DeliveryStatus.DELIVERED
    assert "in_app" in result.channels_attempted
    assert "email" in result.channels_attempted
