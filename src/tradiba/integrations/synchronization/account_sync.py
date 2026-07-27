from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)

class AccountSynchronizer:
    """
    Synchronizes broker account state (balance, equity, margin) 
    with the internal platform state.
    """
    def __init__(self, broker_adapter):
        self.broker = broker_adapter
        self.current_state = {}

    def synchronize(self) -> Dict[str, Any]:
        try:
            account = self.broker.get_account()
            self.current_state = account
            return self.current_state
        except Exception as e:
            logger.error(f"Failed to synchronize account: {e}")
            return self.current_state
