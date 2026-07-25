from fastapi import APIRouter, Depends

from tradiba.api.schemas import NarrativeResponse
from tradiba.api.dependencies import get_narrative_builder
from tradiba.market_structure.narrative_builder import NarrativeBuilder
from tradiba.api.auth.permissions import requires_role

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/narrative", response_model=NarrativeResponse)
async def get_market_narrative(
    symbol: str,
    user: dict = Depends(requires_role("Viewer")),
    builder: NarrativeBuilder = Depends(get_narrative_builder)
):
    # In a real setup, we'd retrieve the Narrative specific to the symbol from a State store
    # Since builder just creates it on the fly, this is a placeholder response assuming state exists
    return NarrativeResponse(
        symbol=symbol,
        trend="BULLISH",
        bias="BUY",
        active_order_blocks=2,
        active_fvgs=1
    )
