from dataclasses import dataclass
from typing import Dict

@dataclass
class PriceLevel:
    price: float
    volume: float
    buy_volume: float
    sell_volume: float

class VolumeProfile:
    """
    Reference Implementation of an Institutional Volume Profile.
    Aggregates traded volume at specific price levels over a given time session.
    """
    
    def __init__(self, tick_size: float = 0.25):
        self.tick_size = tick_size
        self.profile: Dict[float, PriceLevel] = {}
        self.value_area_pct = 0.70 # 70% of volume
        
    def _round_price(self, price: float) -> float:
        """Round price to the nearest tick size."""
        return round(round(price / self.tick_size) * self.tick_size, 2)
        
    def add_trade(self, price: float, volume: float, is_buy: bool):
        """Add a trade to the volume profile."""
        level = self._round_price(price)
        if level not in self.profile:
            self.profile[level] = PriceLevel(level, 0.0, 0.0, 0.0)
            
        self.profile[level].volume += volume
        if is_buy:
            self.profile[level].buy_volume += volume
        else:
            self.profile[level].sell_volume += volume

    def get_poc(self) -> float:
        """Get the Point of Control (POC) - the price level with the highest volume."""
        if not self.profile:
            return 0.0
        return max(self.profile.values(), key=lambda x: x.volume).price

    def get_value_area(self) -> tuple[float, float]:
        """Calculate the Value Area High (VAH) and Value Area Low (VAL)."""
        if not self.profile:
            return (0.0, 0.0)
            
        total_volume = sum(lvl.volume for lvl in self.profile.values())
        target_volume = total_volume * self.value_area_pct
        
        poc_price = self.get_poc()
        current_volume = self.profile[poc_price].volume
        
        sorted_prices = sorted(self.profile.keys())
        poc_idx = sorted_prices.index(poc_price)
        
        up_idx = poc_idx + 1
        down_idx = poc_idx - 1
        
        while current_volume < target_volume:
            vol_up = self.profile[sorted_prices[up_idx]].volume if up_idx < len(sorted_prices) else 0
            vol_down = self.profile[sorted_prices[down_idx]].volume if down_idx >= 0 else 0
            
            if vol_up == 0 and vol_down == 0:
                break
                
            if vol_up > vol_down:
                current_volume += vol_up
                up_idx += 1
            else:
                current_volume += vol_down
                down_idx -= 1
                
        vah = sorted_prices[up_idx - 1] if up_idx > 0 else poc_price
        val = sorted_prices[down_idx + 1] if down_idx < len(sorted_prices) - 1 else poc_price
        
        return (vah, val)
