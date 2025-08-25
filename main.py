from contextlib import asynccontextmanager

import asyncpg
import uvicorn
from fastapi import FastAPI

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.trace import (get_tracer_provider)
from logging import getLogger

from config import settings
from dependencies.database import connect_to_db, disconnect_from_db
from routes import restaurant_route,menu_item_route

if settings.applicationinsights_connection_string:
    configure_azure_monitor(connection_string=settings.applicationinsights_connection_string)

tracer = trace.get_tracer(__name__, tracer_provider=get_tracer_provider())
logger = getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_db()
    yield
    await disconnect_from_db()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
    )

    # Routers
    app.include_router(restaurant_route.router)
    app.include_router(menu_item_route.router)

    return app

app = create_app()
FastAPIInstrumentor.instrument_app(app)

@app.get("/")
async def welcome_user():
    return {"message": "Hello! ESTA user"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
