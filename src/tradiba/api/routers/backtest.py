import asyncio
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from tradiba.api.schemas import BacktestJobResponse, BacktestRequest
from tradiba.api.jobs import job_manager, JobStatus
from tradiba.api.auth.permissions import requires_role

router = APIRouter(prefix="/backtests", tags=["backtests"])


async def mock_backtest_runner(req: BacktestRequest):
    # Simulated delay for backtest
    await asyncio.sleep(2)
    return {"net_profit": 1500.0, "max_drawdown": 5.2}


@router.post("", response_model=BacktestJobResponse)
async def create_backtest(
    request: BacktestRequest,
    user: dict = Depends(requires_role("Admin"))
):
    job_id = job_manager.submit("backtest", mock_backtest_runner(request))
    return BacktestJobResponse(
        id=job_id,
        status="QUEUED",
        strategy=request.strategy,
        symbol=request.symbol,
        progress=0.0
    )


@router.get("/{job_id}", response_model=BacktestJobResponse)
async def get_backtest(job_id: str, user: dict = Depends(requires_role("Viewer"))):
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    return BacktestJobResponse(
        id=job.id,
        status=job.status.value,
        strategy="Unknown", # normally stored in job metadata
        symbol="Unknown",
        progress=job.progress,
        result=job.result
    )


@router.get("", response_model=List[BacktestJobResponse])
async def list_backtests(user: dict = Depends(requires_role("Viewer"))):
    return [
        BacktestJobResponse(
            id=job.id,
            status=job.status.value,
            strategy="Unknown",
            symbol="Unknown",
            progress=job.progress,
            result=job.result
        )
        for job in job_manager.list_jobs("backtest")
    ]


@router.delete("/{job_id}")
async def cancel_backtest(job_id: str, user: dict = Depends(requires_role("Admin"))):
    if job_manager.cancel(job_id):
        return {"status": "cancelled"}
    raise HTTPException(status_code=400, detail="Cannot cancel job")
