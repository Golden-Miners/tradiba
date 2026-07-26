from enum import Enum

class NotificationDestination(Enum):
    EMAIL = "email"
    SLACK = "slack"
    PAGERDUTY = "pagerduty"

class NotificationRouter:
    """Routes notifications based on severity and rules."""
    def __init__(self) -> None:
        self._sent_messages: list[tuple[NotificationDestination, str, str]] = []

    def send(self, destination: NotificationDestination, severity: str, message: str) -> None:
        if severity == "critical" and destination != NotificationDestination.PAGERDUTY:
            # Escalation policy
            self._sent_messages.append((NotificationDestination.PAGERDUTY, severity, message))
        else:
            self._sent_messages.append((destination, severity, message))
            
    def get_sent_messages(self) -> list[tuple[NotificationDestination, str, str]]:
        return self._sent_messages
