from tradiba.notifications.dispatcher import ChannelDispatcher
from tradiba.notifications.models.notification import Notification
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class EmailDispatcher(ChannelDispatcher):
    def get_channel_name(self) -> str:
        return "email"
        
    def dispatch(self, notification: Notification, recipient_contact: Dict[str, Any]) -> bool:
        email_address = recipient_contact.get("email")
        if not email_address:
            logger.warning(f"Failed to dispatch {notification.id}: No email address provided.")
            return False
            
        logger.info(f"[EMAIL] Dispatching to {email_address}: [{notification.severity.value.upper()}] {notification.title}")
        logger.debug(f"[EMAIL Body]: {notification.message}")
        
        # In a real implementation, this would use a library like smtplib, aiosmtplib, or an SDK like SendGrid
        return True
