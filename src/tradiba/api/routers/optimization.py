import asyncio
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from tradiba.api.schemas import BacktestJobResponse, BacktestRequest # reuse schemas for simplicity
from tradiba.api.jobs import job_manager, JobStatus
from tradiba.api.auth.permissions import requires_role

router = APIRouter(prefix="/optimizations", tags=["optimizations"])


async def mock_optimization_runner(req: BacktestRequest):
    await asyncio.sleep(2)
    return {"best_params": {"risk": 2.0}, "score": 150.0}


@router.post("", response_model=BacktestJobResponse)
async def create_optimization(
    request: BacktestRequest,
    user: dict = Depends(requires_role("Admin"))
):
    job_id = job_manager.submit("optimization", mock_optimization_runner(request))
    return BacktestJobResponse(
        id=job_id,
        status="QUEUED",
        strategy=request.strategy,
        symbol=request.symbol,
        progress=0.0
    )


@router.get("/{job_id}", response_model=BacktestJobResponse)
async def get_optimization(job_id: str, user: dict = Depends(requires_role("Viewer"))):
    job = job_manager.get_job(job_id)
    if not job or job.type != "optimization":
        raise HTTPException(status_code=404, detail="Job not found")
        
    return BacktestJobResponse(
        id=job.id,
        status=job.status.value,
        strategy="Unknown",
        symbol="Unknown",
        progress=job.progress,
        result=job.result
    )


@router.get("", response_model=List[BacktestJobResponse])
async def list_optimizations(user: dict = Depends(requires_role("Viewer"))):
    return [
        BacktestJobResponse(
            id=job.id,
            status=job.status.value,
            strategy="Unknown",
            symbol="Unknown",
            progress=job.progress,
            result=job.result
        )
        for job in job_manager.list_jobs("optimization")
    ]


@router.delete("/{job_id}")
async def cancel_optimization(job_id: str, user: dict = Depends(requires_role("Admin"))):
    if job_manager.cancel(job_id):
        return {"status": "cancelled"}
    raise HTTPException(status_code=400, detail="Cannot cancel job")
