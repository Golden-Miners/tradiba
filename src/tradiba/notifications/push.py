from tradiba.notifications.dispatcher import ChannelDispatcher
from tradiba.notifications.models.notification import Notification
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class PushDispatcher(ChannelDispatcher):
    def get_channel_name(self) -> str:
        return "push"
        
    def dispatch(self, notification: Notification, recipient_contact: Dict[str, Any]) -> bool:
        device_tokens = recipient_contact.get("device_tokens", [])
        if not device_tokens:
            logger.warning(f"Failed to dispatch {notification.id}: No device tokens provided.")
            return False
            
        for token in device_tokens:
            logger.info(f"[PUSH] Dispatching to device {token[-6:]}: {notification.title}")
            
        # Real implementation would use Firebase Cloud Messaging (FCM) or Apple Push Notification Service (APNs)
        return True
