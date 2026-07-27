from typing import List
import logging

from tradiba.integrations.brokers.base import BrokerAdapter

logger = logging.getLogger(__name__)

class FailoverManager:
    """
    Manages failover policies and routes requests to a secondary 
    broker if the primary broker fails.
    """
    def __init__(self, primary: BrokerAdapter, secondaries: List[BrokerAdapter]):
        self.primary = primary
        self.secondaries = secondaries
        self.active_adapter = primary

    def check_health(self) -> bool:
        """
        Check if the active adapter is healthy. If not, trigger failover.
        """
        try:
            # We assume connect() or a ping method validates health
            is_healthy = self.active_adapter.connect()
            if not is_healthy:
                self._trigger_failover()
            return is_healthy
        except Exception as e:
            logger.error(f"Health check failed on {self.active_adapter}: {e}")
            self._trigger_failover()
            return False

    def _trigger_failover(self):
        logger.warning(f"Triggering failover from {self.active_adapter}")
        
        for secondary in self.secondaries:
            try:
                if secondary.connect():
                    self.active_adapter = secondary
                    logger.info(f"Successfully failed over to {secondary}")
                    return
            except Exception as e:
                logger.error(f"Failed to connect to secondary {secondary}: {e}")
                
        logger.critical("All brokers unavailable. System halted.")
        
    def get_active_adapter(self) -> BrokerAdapter:
        return self.active_adapter
