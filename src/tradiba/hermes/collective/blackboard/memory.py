import asyncio
from typing import Dict, Any

class BlackboardMemory:
    """
    Shared workspace for the Collective.
    Contains:
    - Current market state
    - Active goals
    - Research findings
    - Open risks
    - Proposed actions
    - Evidence references
    
    Thread/Async-safe via asyncio.Lock.
    """
    
    def __init__(self):
        self._lock = asyncio.Lock()
        self._state: Dict[str, Any] = {
            "market_state": {},
            "active_goals": [],
            "research_findings": [],
            "open_risks": [],
            "proposed_actions": [],
            "evidence": {}
        }

    async def get_all(self) -> Dict[str, Any]:
        async with self._lock:
            return dict(self._state)

    async def get_section(self, section: str) -> Any:
        async with self._lock:
            return self._state.get(section)

    async def update_market_state(self, updates: Dict[str, Any]):
        async with self._lock:
            self._state["market_state"].update(updates)

    async def append_research_finding(self, finding: Dict[str, Any]):
        async with self._lock:
            self._state["research_findings"].append(finding)

    async def append_proposed_action(self, action: Dict[str, Any]):
        async with self._lock:
            self._state["proposed_actions"].append(action)

    async def append_open_risk(self, risk: Dict[str, Any]):
        async with self._lock:
            self._state["open_risks"].append(risk)

    async def add_evidence(self, key: str, evidence: Any):
        async with self._lock:
            self._state["evidence"][key] = evidence
            
    async def add_active_goal(self, goal: Dict[str, Any]):
        async with self._lock:
            self._state["active_goals"].append(goal)
