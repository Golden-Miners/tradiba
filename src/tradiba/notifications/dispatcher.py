from abc import ABC, abstractmethod
from typing import Dict, Any
from tradiba.notifications.models.notification import Notification

class ChannelDispatcher(ABC):
    """Abstract interface for dispatching notifications to a specific channel."""
    
    @abstractmethod
    def get_channel_name(self) -> str:
        """Returns the identifier for this channel (e.g., 'email', 'push')."""
        pass
        
    @abstractmethod
    def dispatch(self, notification: Notification, recipient_contact: Dict[str, Any]) -> bool:
        """
        Dispatches the notification.
        Returns True if successfully dispatched, False otherwise.
        """
        pass
