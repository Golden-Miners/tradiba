from tradiba.events import DomainEvent
from typing import Dict, Any

class NotificationCreatedEvent(DomainEvent):
    def __init__(self, notification_id: str, recipient_id: str, severity: str):
        super().__init__()
        self.notification_id = notification_id
        self.recipient_id = recipient_id
        self.severity = severity

class NotificationDeliveredEvent(DomainEvent):
    def __init__(self, notification_id: str, channel: str):
        super().__init__()
        self.notification_id = notification_id
        self.channel = channel

class AutomationRuleTriggeredEvent(DomainEvent):
    def __init__(self, rule_name: str, event_data: Dict[str, Any]):
        super().__init__()
        self.rule_name = rule_name
        self.event_data = event_data
