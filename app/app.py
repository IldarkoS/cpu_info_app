import psutil

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates  

from app.database import Base, engine
from app.routers import system_metrics, dashboard

app = FastAPI()

app.include_router(system_metrics.router)
app.include_router(dashboard.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
