import psutil
import functools

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from asyncio import events
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.system_metrics import SystemMetrics

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


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


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api/async_info")
async def get_async_info(db: AsyncSession = Depends(get_db)):
    cpu_percent = psutil.cpu_percent(interval=None)
    memory_percent = psutil.virtual_memory().percent
    cpu_freq = psutil.cpu_freq().current

    data = {
        "cpu_times": psutil.cpu_times()._asdict(),
        "cpu_percent": cpu_percent,
        "cpu_frequencies": cpu_freq,
        "memory_percent": memory_percent,
        "cpu_stats": psutil.cpu_stats()._asdict(),
        "load_avg": {i: x / psutil.cpu_count() * 100 for i, x in enumerate(psutil.getloadavg(), start=1)},
        "memory_info": psutil.virtual_memory()._asdict(),
        "swap_memory": psutil.swap_memory()._asdict()
    }

    new_entry = SystemMetrics(
        cpu_percent=cpu_percent,
        cpu_frequencies=cpu_freq,
        memory_percent=memory_percent,
        cpu_times=data["cpu_times"],
        cpu_stats=data["cpu_stats"],
        load_avg=data["load_avg"],
        memory_info=data["memory_info"],
        swap_memory=data["swap_memory"]
    )
    db.add(new_entry)
    await db.commit()

    return {
        "cpu_percent": cpu_percent,
        "memory_percent": memory_percent,
        "cpu_freq": cpu_freq
    }


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
