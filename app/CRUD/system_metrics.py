from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.system_metrics import SystemMetrics
from app.schemas.system_metrics import SystemMetricsCreate

async def create_system_metrics(db: AsyncSession, metrics: SystemMetricsCreate):
    db_entry = SystemMetrics(**metrics)
    db.add(db_entry)
    await db.commit()
    await db.refresh(db_entry)
    return db_entry

async def get_all_metrics(db: AsyncSession):
    result = await db.execute(select(SystemMetrics))
    return result.scalars().all()