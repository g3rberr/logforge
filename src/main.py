from fastapi import FastAPI

from api.v1.analytics import router as analytics_router
from api.v1.auth import router as auth_router
from api.v1.ingest import router as ingest_router
from api.v1.projects import router as projects_router

app = FastAPI(title="logforge", version="0.1.0")

app.include_router(auth_router, prefix="/api/v1")
app.include_router(ingest_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")
app.include_router(projects_router, prefix="/api/v1")
