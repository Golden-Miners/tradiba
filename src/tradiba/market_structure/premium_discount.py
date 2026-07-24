"""
Premium / Discount calculation utility.
"""

from enum import Enum
from tradiba.market_structure.models import SwingPoint


class PDZone(Enum):
    PREMIUM = "PREMIUM"
    DISCOUNT = "DISCOUNT"
    EQUILIBRIUM = "EQUILIBRIUM"


def compute_premium_discount(price: float, swing_high: SwingPoint | None, swing_low: SwingPoint | None) -> PDZone | None:
    """
    Computes whether the current price is in a Premium or Discount zone
    based on the most recent swing high and low.
    
    Premium: price > equilibrium (upper 50%)
    Discount: price < equilibrium (lower 50%)
    Equilibrium: price == equilibrium
    """
    if not swing_high or not swing_low:
        return None
    
    # If the swings are inverted (should not happen in normal market structure)
    high_price = max(swing_high.price, swing_low.price)
    low_price = min(swing_high.price, swing_low.price)
    
    equilibrium = (high_price + low_price) / 2.0
    
    if price > equilibrium:
        return PDZone.PREMIUM
    elif price < equilibrium:
        return PDZone.DISCOUNT
    else:
        return PDZone.EQUILIBRIUM
