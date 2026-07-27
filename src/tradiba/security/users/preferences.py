from typing import Dict, Any
from pydantic import BaseModel, Field

class DashboardLayout(BaseModel):
    panels: list = Field(default_factory=list)
    active_workspace: str = "default"

class UserPreferences(BaseModel):
    user_id: str
    theme: str = "dark"
    time_zone: str = "UTC"
    notifications_enabled: bool = True
    favorite_symbols: list = Field(default_factory=list)
    layout: DashboardLayout = Field(default_factory=DashboardLayout)

class PreferencesService:
    """Manages user-specific preferences and layout configurations."""
    def __init__(self):
        self._store: Dict[str, UserPreferences] = {}
        
    def get_preferences(self, user_id: str) -> UserPreferences:
        if user_id not in self._store:
            self._store[user_id] = UserPreferences(user_id=user_id)
        return self._store[user_id]
        
    def update_preferences(self, user_id: str, updates: Dict[str, Any]) -> UserPreferences:
        prefs = self.get_preferences(user_id)
        updated_data = {**prefs.model_dump(), **updates}
        new_prefs = UserPreferences(**updated_data)
        self._store[user_id] = new_prefs
        return new_prefs
