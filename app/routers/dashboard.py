from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates

from app.database import get_db
from app.CRUD.system_metrics import get_all_metrics
from app.core.monitoring import collect_system_metrics

router = APIRouter(tags=["Dashboard"])

templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@router.get("/api/metrics")
async def api_metrics():
    metrics = collect_system_metrics()
    return metrics