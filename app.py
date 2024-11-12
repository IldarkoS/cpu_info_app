import logging
import contextvars
import functools
from asyncio import events
from typing import Dict

from fastapi import FastAPI
import psutil
from pydantic import BaseModel

app = FastAPI()


class SyncInfoResponse(BaseModel):
    cpu_times: Dict[str, float]
    cpu_percent: float
    cpu_count_physical_cores: int
    cpu_count_all_cores: int
    cpu_stats: Dict[str, int]
    cpu_frequencies: float
    load_avg: Dict[int, float]
    memory_info: Dict[str, int]
    swap_memory: Dict[str, int]


@app.get("/sync_info", response_model=SyncInfoResponse)
def get_sync_info() -> SyncInfoResponse:

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


class AsyncInfoResponse(BaseModel):
    cpu_times: Dict[str, float]
    cpu_percent: float
    cpu_count_physical_cores: int
    cpu_count_all_cores: int
    cpu_stats: Dict[str, int]
    cpu_frequencies: float
    load_avg: Dict[int, float]
    memory_info: Dict[str, float]
    swap_memory: Dict[str, int]


async def get_async_info() -> AsyncInfoResponse:

    loop = events.get_running_loop()
    contextvars.copy_context()

    cpu_times = await loop.run_in_executor(None, functools.partial(psutil.cpu_times))
    cpu_percent = await loop.run_in_executor(None, functools.partial(psutil.cpu_percent))
    cpu_count_physical_cores = await loop.run_in_executor(None, functools.partial(psutil.cpu_count, logical=False))
    cpu_count_all_cores = await loop.run_in_executor(None, functools.partial(psutil.cpu_count, logical=False))
    cpu_stats = await loop.run_in_executor(None, functools.partial(psutil.cpu_stats))
    cpu_frequencies = await loop.run_in_executor(None, functools.partial(psutil.cpu_freq))
    load_avg = {i: x / psutil.cpu_count() * 100 for i, x in enumerate(psutil.getloadavg(), start=1)}
    memory_info = psutil.virtual_memory()
    swap_memory = await loop.run_in_executor(None, functools.partial(psutil.swap_memory))

    return AsyncInfoResponse(
        cpu_times=cpu_times._asdict(),
        cpu_percent=cpu_percent,
        cpu_count_physical_cores=cpu_count_physical_cores,
        cpu_count_all_cores=cpu_count_all_cores,
        cpu_stats=cpu_stats._asdict(),
        cpu_frequencies=cpu_frequencies.current,
        load_avg=load_avg,
        memory_info=memory_info._asdict(),
        swap_memory=swap_memory._asdict()
    )


@app.get("/async_info", response_model=AsyncInfoResponse)
async def get_async_info_route() -> AsyncInfoResponse:
    return await get_async_info()
