from tradiba.events import DomainEvent
from typing import List

class UserCreatedEvent(DomainEvent):
    def __init__(self, user_id: str, username: str):
        super().__init__()
        self.user_id = user_id
        self.username = username

class UserLoggedInEvent(DomainEvent):
    def __init__(self, user_id: str, session_id: str, ip_address: str):
        super().__init__()
        self.user_id = user_id
        self.session_id = session_id
        self.ip_address = ip_address

class UserLoggedOutEvent(DomainEvent):
    def __init__(self, user_id: str, session_id: str):
        super().__init__()
        self.user_id = user_id
        self.session_id = session_id

class RoleAssignedEvent(DomainEvent):
    def __init__(self, user_id: str, roles: List[str]):
        super().__init__()
        self.user_id = user_id
        self.roles = roles

class ApiKeyCreatedEvent(DomainEvent):
    def __init__(self, user_id: str, key_id: str):
        super().__init__()
        self.user_id = user_id
        self.key_id = key_id

class SessionExpiredEvent(DomainEvent):
    def __init__(self, session_id: str):
        super().__init__()
        self.session_id = session_id

class MfaEnabledEvent(DomainEvent):
    def __init__(self, user_id: str):
        super().__init__()
        self.user_id = user_id
