import functools
from asyncio import events
from typing import Dict

from fastapi import FastAPI
import psutil
from pydantic import BaseModel

app = FastAPI()


class InfoResponse(BaseModel):
    cpu_times: Dict[str, float]
    cpu_percent: float
    cpu_count_physical_cores: int
    cpu_count_all_cores: int
    cpu_stats: Dict[str, int]
    cpu_frequencies: float
    load_avg: Dict[int, float]
    memory_info: Dict[str, float]
    swap_memory: Dict[str, float]


@app.get("/sync_info", response_model=InfoResponse)
def get_sync_info() -> InfoResponse:
    return {
        "cpu_times": psutil.cpu_times()._asdict(),
        "cpu_percent": psutil.cpu_percent(interval=None),
        "cpu_count_physical_cores": psutil.cpu_count(logical=False),
        "cpu_count_all_cores": psutil.cpu_count(logical=True),
        "cpu_stats": psutil.cpu_stats()._asdict(),
        "cpu_frequencies": psutil.cpu_freq().current,
        "load_avg": {i: x / psutil.cpu_count() * 100 for i, x in enumerate(psutil.getloadavg(), start=1)},
        "memory_info": psutil.virtual_memory()._asdict(),
        "swap_memory": psutil.swap_memory()._asdict()
    }


@app.get("/async_info", response_model=InfoResponse)
async def get_async_info() -> InfoResponse:
    loop = events.get_running_loop()

    cpu_times, cpu_percent, cpu_stats, cpu_frequencies, swap_memory = await loop.run_in_executor(
        None,
        lambda: (
            psutil.cpu_times()._asdict(),
            psutil.cpu_percent(interval=None),
            psutil.cpu_stats()._asdict(),
            psutil.cpu_freq().current,
            psutil.swap_memory()._asdict()
        )
    )

    load_avg = {i: x / psutil.cpu_count() * 100 for i, x in enumerate(psutil.getloadavg(), start=1)}
    memory_info = psutil.virtual_memory()._asdict()

    return InfoResponse(
        cpu_times=cpu_times,
        cpu_percent=cpu_percent,
        cpu_count_physical_cores=psutil.cpu_count(logical=False),
        cpu_count_all_cores=psutil.cpu_count(logical=True),
        cpu_stats=cpu_stats,
        cpu_frequencies=cpu_frequencies,
        load_avg=load_avg,
        memory_info=memory_info,
        swap_memory=swap_memory
    )
