from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.database import get_db
from app.schemas.system_metrics import SystemMetricsResponse
from app.CRUD.system_metrics import create_system_metrics, get_all_metrics, get_metrics_by_time
from app.core.monitoring import collect_system_metrics


router = APIRouter(prefix="/metrics", tags=["System Metrics"])

@router.get("/", response_model=list[SystemMetricsResponse])
async def read_metrics(db: AsyncSession = Depends(get_db)):
    return await get_all_metrics(db)


@router.post("/", response_model=SystemMetricsResponse)
async def create_metrics(db: AsyncSession = Depends(get_db)):
    metrics_data = collect_system_metrics()
    return await create_system_metrics(db, metrics_data)


@router.get("/analytics")
async def get_analytics(
    start_time: datetime = Query(None),
    end_time: datetime = Query(None),
    db: AsyncSession = Depends(get_db)
):
    if not end_time:
        end_time = datetime.utcnow()
    if not start_time:
        start_time = end_time - timedelta(days=1)

    metrics = await get_metrics_by_time(db, start_time, end_time)

    if not metrics:
        return {"message": "No data for the selected period"}
    
    cpu_percent_values = [m.cpu_percent for m in metrics]
    memory_percent_values = [m.memory_percent for m in metrics]
    freq_values = [m.cpu_frequencies for m in metrics]

    analytics = {
        "cpu_percent": {
            "average": sum(cpu_percent_values) / len(cpu_percent_values),
            "max": max(cpu_percent_values),
            "min": min(cpu_percent_values)
        },
        "memory_percent": {
            "average": sum(memory_percent_values) / len(memory_percent_values),
            "max": max(memory_percent_values),
            "min": min(memory_percent_values)
        },
        "cpu_frequencies": {
            "average": sum(freq_values) / len(freq_values),
            "max": max(freq_values),
            "min": min(freq_values)
        }
    }
    return analytics