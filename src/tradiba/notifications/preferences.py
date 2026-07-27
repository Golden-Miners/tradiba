from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from tradiba.notifications.models.notification import NotificationSeverity
from datetime import time, datetime

class NotificationPreferences(BaseModel):
    user_id: str
    enabled_channels: List[str] = Field(default_factory=lambda: ["in_app", "email"])
    min_severity_for_push: NotificationSeverity = NotificationSeverity.CRITICAL
    quiet_hours_start: Optional[time] = None
    quiet_hours_end: Optional[time] = None
    timezone: str = "UTC"
    
    def in_quiet_hours(self, current_time: datetime) -> bool:
        """Determines if the user is currently in quiet hours."""
        if not self.quiet_hours_start or not self.quiet_hours_end:
            return False
            
        current = current_time.time()
        if self.quiet_hours_start <= self.quiet_hours_end:
            return self.quiet_hours_start <= current <= self.quiet_hours_end
        else:
            # Spans midnight
            return current >= self.quiet_hours_start or current <= self.quiet_hours_end

class PreferencesService:
    def __init__(self):
        # In-memory store for scaffolding
        self._store: Dict[str, NotificationPreferences] = {}
        
    def get_preferences(self, user_id: str) -> NotificationPreferences:
        if user_id not in self._store:
            self._store[user_id] = NotificationPreferences(user_id=user_id)
        return self._store[user_id]
        
    def update_preferences(self, user_id: str, updates: Dict) -> NotificationPreferences:
        prefs = self.get_preferences(user_id)
        updated = {**prefs.model_dump(), **updates}
        new_prefs = NotificationPreferences(**updated)
        self._store[user_id] = new_prefs
        return new_prefs
