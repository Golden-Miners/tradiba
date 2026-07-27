from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from datetime import datetime
from tradiba.integrations.brokers.mt5.service import MT5Service
from tradiba.integrations.brokers.mt5.timeframes import Timeframe

router = APIRouter(prefix="/api/market", tags=["Market Data"])

# Global or injected instance (for MVP we'll just instantiate or fetch a singleton)
mt5_service = MT5Service()

@router.get("/candles")
async def get_candles(symbol: str = "XAUUSD", timeframe: str = "M5", count: int = 100):
    if not mt5_service.connected:
        mt5_service.start()
        
    try:
        tf = Timeframe[timeframe]
        candles = mt5_service.get_recent_candles(symbol, tf, count)
        return [
            {
                "time": int(c.timestamp.timestamp()),
                "open": c.open,
                "high": c.high,
                "low": c.low,
                "close": c.close,
                "volume": c.tick_volume
            }
            for c in candles
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
