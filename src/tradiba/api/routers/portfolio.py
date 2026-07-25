from typing import List
from fastapi import APIRouter, Depends

from tradiba.api.schemas import PortfolioResponse, PositionResponse
from tradiba.api.dependencies import get_portfolio_service
from tradiba.portfolio.service import PortfolioService
from tradiba.api.auth.permissions import requires_role

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("", response_model=PortfolioResponse)
async def get_portfolio_summary(
    user: dict = Depends(requires_role("Trader")),
    service: PortfolioService = Depends(get_portfolio_service)
):
    portfolio = service.repository.load()
    if not portfolio:
        return PortfolioResponse(
            equity=0.0,
            balance=0.0,
            free_margin=0.0,
            positions_count=0
        )
    return PortfolioResponse(
        equity=portfolio.equity,
        balance=portfolio.balance,
        free_margin=portfolio.free_margin,
        positions_count=portfolio.open_positions
    )


@router.get("/positions", response_model=List[PositionResponse])
async def get_active_positions(
    user: dict = Depends(requires_role("Trader")),
    service: PortfolioService = Depends(get_portfolio_service)
):
    # We return empty list as Portfolio aggregate doesn't track detailed positions in the requested struct
    # In a full implementation, we'd query an ExecutionRepository or similar read model.
    return []
