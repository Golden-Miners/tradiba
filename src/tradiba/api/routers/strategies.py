from typing import List
from fastapi import APIRouter, Depends, HTTPException

from tradiba.api.schemas import StrategyResponse
from tradiba.api.dependencies import get_strategy_engine
from tradiba.strategy.engine import StrategyEngine
from tradiba.api.auth.permissions import requires_role

router = APIRouter(prefix="/strategies", tags=["strategies"])


@router.get("", response_model=List[StrategyResponse])
async def list_strategies(
    user: dict = Depends(requires_role("Viewer")),
    engine: StrategyEngine = Depends(get_strategy_engine)
):
    # Depending on how strategies are tracked in engine
    # we assume engine._strategies dict exists for this snippet
    return [
        StrategyResponse(
            name=name,
            enabled=True, # We'll just assume they are enabled if loaded
            description=str(type(strategy).__name__)
        )
        for name, strategy in getattr(engine, "_strategies", {}).items()
    ]


@router.post("/{name}/enable")
async def enable_strategy(
    name: str,
    user: dict = Depends(requires_role("Admin")),
    engine: StrategyEngine = Depends(get_strategy_engine)
):
    # Mock endpoint for enabling
    return {"status": f"Strategy {name} enabled."}


@router.post("/{name}/disable")
async def disable_strategy(
    name: str,
    user: dict = Depends(requires_role("Admin")),
    engine: StrategyEngine = Depends(get_strategy_engine)
):
    # Mock endpoint for disabling
    return {"status": f"Strategy {name} disabled."}
