import json
import asyncio
from typing import List
from fastapi import WebSocket
from tradiba.events import EventBus, DomainEvent
from tradiba.integrations.brokers.mt5.service import MT5Service

@dataclass
class MarketTickEvent(DomainEvent):
    def __init__(self, timestamp: float, payload: dict):
        super().__init__("MarketTickEvent", timestamp, payload)


class WebSocketManager:
    """Manages WebSocket connections and bridges EventBus events to clients."""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.active_connections: List[WebSocket] = []
        # In a real setup, we'd register a generic handler or specific handlers 
        # on the event_bus to forward events to a queue here.
        # For this skeleton, we'll run a background task if needed or mock it.
        self._queue = asyncio.Queue()
        # Assume we subscribe to all events for broadcasting
        # self.event_bus.subscribe(DomainEvent, self._handle_event)
        
    def _handle_event(self, event: DomainEvent) -> None:
        # We push to the async queue so we don't block sync event bus execution
        # (Assuming the event bus handler is called synchronously)
        try:
            self._queue.put_nowait(event)
        except asyncio.QueueFull:
            pass

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                # Connection dropped
                pass
                
    async def run_broadcaster(self):
        """Background task to pull events from queue and broadcast them."""
        while True:
            try:
                event = await asyncio.wait_for(self._queue.get(), timeout=1.0)
                msg = json.dumps({
                    "type": event.__class__.__name__,
                    "payload": getattr(event, "__dict__", {})
                }, default=str)
                await self.broadcast(msg)
            except asyncio.TimeoutError:
                pass

    async def run_market_poller(self):
        """Polls MT5 for XAUUSD ticks and emits them to WS."""
        mt5_service = MT5Service()
        if not mt5_service.connected:
            try:
                mt5_service.start()
            except Exception as e:
                print(f"Failed to connect to MT5: {e}")
                return
                
        last_price = 0
        while True:
            try:
                tick = mt5_service.get_tick("XAUUSD")
                if tick and tick.last != last_price:
                    last_price = tick.last
                    msg = json.dumps({
                        "type": "MarketTickEvent",
                        "payload": {
                            "symbol": "XAUUSD",
                            "price": tick.last,
                            "time": int(tick.timestamp.timestamp())
                        }
                    })
                    await self.broadcast(msg)
            except Exception as e:
                pass
            await asyncio.sleep(1)


# A global instance is typically used, or injected via app state
ws_manager: WebSocketManager | None = None

def setup_websockets(event_bus: EventBus) -> WebSocketManager:
    global ws_manager
    ws_manager = WebSocketManager(event_bus)
    # Start broadcaster
    asyncio.create_task(ws_manager.run_broadcaster())
    asyncio.create_task(ws_manager.run_market_poller())
    return ws_manager
