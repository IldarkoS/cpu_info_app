from typing import Dict, Any
from pydantic import BaseModel
from datetime import datetime

class SystemMetricsBase(BaseModel):
    cpu_percent: float
    cpu_frequencies: float
    memory_percent: float
    cpu_times: Dict[str, float]
    cpu_stats: Dict[str, int]
    load_avg: Dict[int, float]
    memory_info: Dict[str, float]
    swap_memory: Dict[str, float]

class SystemMetricsCreate(SystemMetricsBase):
    pass

class SystemMetricsResponse(SystemMetricsBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
        from_attributes=True