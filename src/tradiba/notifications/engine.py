from tradiba.notifications.models.notification import Notification, DeliveryStatus
from tradiba.notifications.dispatcher import ChannelDispatcher
from tradiba.notifications.preferences import PreferencesService
from typing import Dict, List, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class NotificationEngine:
    def __init__(self, preferences_service: PreferencesService, dispatchers: List[ChannelDispatcher]):
        self.prefs = preferences_service
        self.dispatchers = {d.get_channel_name(): d for d in dispatchers}
        
    def dispatch_notification(self, notification: Notification, recipient_contact: Dict[str, Any]) -> Notification:
        user_prefs = self.prefs.get_preferences(notification.recipient_id)
        current_time = datetime.utcnow()
        
        # Check quiet hours unless emergency
        if notification.severity.value != "emergency" and user_prefs.in_quiet_hours(current_time):
            logger.info(f"Skipping dispatch for {notification.id}: User in quiet hours.")
            notification.status = DeliveryStatus.PENDING
            return notification
            
        successes = 0
        
        # Always try in-app (doesn't require external dispatch, just saving to DB in a real app)
        if "in_app" in user_prefs.enabled_channels:
            successes += 1
            notification.channels_attempted.append("in_app")
            
        # Try external channels
        for channel in user_prefs.enabled_channels:
            if channel == "in_app" or channel not in self.dispatchers:
                continue
                
            dispatcher = self.dispatchers[channel]
            success = dispatcher.dispatch(notification, recipient_contact)
            notification.channels_attempted.append(channel)
            
            if success:
                successes += 1
                
        if successes > 0:
            notification.status = DeliveryStatus.DELIVERED
        else:
            notification.status = DeliveryStatus.FAILED
            
        return notification
