from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.system_metrics import SystemMetricsResponse
from app.CRUD.system_metrics import create_system_metrics, get_all_metrics
from app.core.monitoring import collect_system_metrics

router = APIRouter(prefix="/metrics", tags=["System Metrics"])

@router.get("/", response_model=list[SystemMetricsResponse])
async def read_metrics(db: AsyncSession = Depends(get_db)):
    return await get_all_metrics(db)

@router.post("/", response_model=SystemMetricsResponse)
async def create_metrics(db: AsyncSession = Depends(get_db)):
    metrics_data = collect_system_metrics()
    return await create_system_metrics(db, metrics_data)