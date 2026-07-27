import asyncio
from typing import Dict, Any, Callable, List
import uuid

class CommunicationBus:
    """
    Supports:
    - Publish/Subscribe
    - Request/Response
    - Broadcast
    """
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._message_history: List[Dict[str, Any]] = []
        self._lock = asyncio.Lock()

    async def subscribe(self, topic: str, callback: Callable):
        async with self._lock:
            if topic not in self._subscribers:
                self._subscribers[topic] = []
            self._subscribers[topic].append(callback)

    async def publish(self, topic: str, sender: str, payload: Dict[str, Any]):
        msg = {
            "id": str(uuid.uuid4()),
            "topic": topic,
            "sender": sender,
            "payload": payload,
            "type": "PUBLISH"
        }
        async with self._lock:
            self._message_history.append(msg)
            callbacks = self._subscribers.get(topic, [])
            
        for cb in callbacks:
            if asyncio.iscoroutinefunction(cb):
                await cb(msg)
            else:
                cb(msg)

    async def broadcast(self, sender: str, payload: Dict[str, Any]):
        msg = {
            "id": str(uuid.uuid4()),
            "topic": "*",
            "sender": sender,
            "payload": payload,
            "type": "BROADCAST"
        }
        async with self._lock:
            self._message_history.append(msg)
            callbacks = []
            for subs in self._subscribers.values():
                callbacks.extend(subs)
                
        # Deduplicate callbacks
        unique_cbs = list(set(callbacks))
        for cb in unique_cbs:
            if asyncio.iscoroutinefunction(cb):
                await cb(msg)
            else:
                cb(msg)

    async def get_history(self) -> List[Dict[str, Any]]:
        async with self._lock:
            return list(self._message_history)
