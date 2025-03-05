from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime

from app.models.system_metrics import SystemMetrics
from app.schemas.system_metrics import SystemMetricsCreate, SystemMetricsResponse

async def create_system_metrics(db: AsyncSession, metrics: SystemMetricsCreate):
    db_entry = SystemMetrics(**metrics)
    db.add(db_entry)
    await db.commit()
    await db.refresh(db_entry)
    return db_entry

async def get_all_metrics(db: AsyncSession):
    result = await db.execute(select(SystemMetrics))
    return result.scalars().all()


async def get_metrics_by_time(db: AsyncSession, start_time: datetime, end_time: datetime):
    query = select(SystemMetrics).where(
        and_(
            SystemMetrics.timestamp >= start_time,
            SystemMetrics.timestamp <= end_time
        )
    )
    result = await db.execute(query)
    metrics = result.scalars().all()
    return [SystemMetricsResponse.from_orm(metric) for metric in metrics]
