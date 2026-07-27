from tradiba.notifications.dispatcher import ChannelDispatcher
from tradiba.notifications.models.notification import Notification
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class WebhookDispatcher(ChannelDispatcher):
    def get_channel_name(self) -> str:
        return "webhook"
        
    def dispatch(self, notification: Notification, recipient_contact: Dict[str, Any]) -> bool:
        webhook_urls = recipient_contact.get("webhooks", [])
        if not webhook_urls:
            return False
            
        payload = {
            "id": notification.id,
            "type": notification.type,
            "severity": notification.severity,
            "title": notification.title,
            "message": notification.message,
            "metadata": notification.metadata
        }
        
        for url in webhook_urls:
            logger.info(f"[WEBHOOK] POST {url} for {notification.id} payload={payload}")
            # Real implementation would use httpx or requests to send the payload
            
        return True
