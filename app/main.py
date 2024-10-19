import os
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.database.database_setup import create_db
from dotenv import load_dotenv
import logging

from app.exceptions.exception_handlers import request_validation_exception_handler, uncovered_area_exception_handler, unexpected_geometry_exception_handler
from app.models.exception_model import UncoveredAreaException, UnexpectedGeometryException
from app.routers.terrain_router import router as terrain_split_router
from app.routers.health import router as health_router

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(
        title="TerrainApp",
        description="An app for splitting up the building limits according to the height plateaus",
        version="1.0.0",
    )

    # random security setup...
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # exception handling
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(UncoveredAreaException, uncovered_area_exception_handler)
    app.add_exception_handler(UnexpectedGeometryException, unexpected_geometry_exception_handler)

    # all routers
    app.include_router(health_router, prefix="/health", tags=["Status"])
    app.include_router(terrain_split_router, prefix="/terrain", tags=["Terrain"])

    # setup database tables if they dont exitst. This should probably be improved at some point. 
    create_db()

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting the application...")
    uvicorn.run(app, host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", 8000)))