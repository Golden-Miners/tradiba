import sys
from unittest.mock import MagicMock

# Mock MetaTrader5 before any local imports happen
sys.modules['MetaTrader5'] = MagicMock()
