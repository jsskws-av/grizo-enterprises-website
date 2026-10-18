"""
AI E-Commerce Research, Listing & Management System (Amazon India)
Main Application Server (FastAPI + Uvicorn)
Zero-build standalone architecture serving a modern responsive web dashboard.
"""

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config.settings import settings, BASE_DIR
from database.connection import init_db
from database.seed_data import seed_database
from scheduler.daily_runner import daily_scheduler

# Routers
from api.routes_auth import router as auth_router
from api.routes_products import router as products_router
from api.routes_calculator import router as calculator_router
from api.routes_approvals import router as approvals_router
from api.routes_inventory import router as inventory_router
from api.routes_listings import router as listings_router
from api.routes_reports import router as reports_router
from api.routes_integrations import router as integrations_router
from api.routes_system import router as system_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure tables exist and seed baseline data
    seed_database()
    print("✓ E-Commerce Automation Platform initialized successfully.")
    yield
    # Shutdown: Stop scheduler
    daily_scheduler.stop()
    print("Platform safely shut down.")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(calculator_router)
app.include_router(approvals_router)
app.include_router(inventory_router)
app.include_router(listings_router)
app.include_router(reports_router)
app.include_router(integrations_router)
app.include_router(system_router)

# Mount Static Files
STATIC_DIR = BASE_DIR / "web" / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

INDEX_PATH = BASE_DIR / "web" / "templates" / "index.html"


@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    if INDEX_PATH.exists():
        return FileResponse(INDEX_PATH)
    return HTMLResponse("<h2>Dashboard is loading...</h2>")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
