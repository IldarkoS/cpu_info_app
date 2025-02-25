from app.database import Base
from sqlalchemy import Column, Integer, Float, JSON, DateTime
from sqlalchemy.sql import func


class SystemMetrics(Base):
    __tablename__ = "system_metrics"
    id = Column(Integer, primary_key=True, index=True)
    cpu_percent = Column(Float)
    cpu_frequencies = Column(Float)
    memory_percent = Column(Float)
    cpu_times = Column(JSON)
    cpu_stats = Column(JSON)
    load_avg = Column(JSON)
    memory_info = Column(JSON)
    swap_memory = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())