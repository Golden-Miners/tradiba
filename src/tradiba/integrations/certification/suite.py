import logging
from tradiba.integrations.brokers.base import BrokerAdapter

logger = logging.getLogger(__name__)

class AdapterCertificationSuite:
    """
    Runs certification tests against an adapter to ensure it complies
    with the required interfaces and resilience policies.
    """
    
    def __init__(self, adapter: BrokerAdapter):
        self.adapter = adapter

    def run_all(self) -> bool:
        logger.info(f"Starting certification for {self.adapter.__class__.__name__}")
        results = [
            self.test_connection(),
            self.test_account_retrieval(),
            self.test_positions_retrieval(),
        ]
        
        success = all(results)
        if success:
            logger.info("Certification PASSED")
        else:
            logger.error("Certification FAILED")
            
        return success

    def test_connection(self) -> bool:
        try:
            res = self.adapter.connect()
            return res is not None
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
            
    def test_account_retrieval(self) -> bool:
        try:
            account = self.adapter.get_account()
            return isinstance(account, dict)
        except Exception as e:
            logger.error(f"Account retrieval test failed: {e}")
            return False
            
    def test_positions_retrieval(self) -> bool:
        try:
            positions = self.adapter.get_positions()
            return isinstance(positions, list)
        except Exception as e:
            logger.error(f"Positions retrieval test failed: {e}")
            return False
