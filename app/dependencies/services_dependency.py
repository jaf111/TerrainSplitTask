from typing import Annotated
from fastapi import Depends

from app.services.terrain_service import TerrainService
from app.services.terrain_visualize_service import TerrainVisualizeService
from app.database.database_service import DatabaseService


def get_database_service() -> DatabaseService:
    return DatabaseService()

DatabaseServiceDep = Annotated[DatabaseService, Depends(get_database_service)]


def get_terrain_service(database_service: DatabaseServiceDep) -> TerrainService:
    return TerrainService(database_service)

TerrainServiceDep = Annotated[TerrainService, Depends(get_terrain_service)]


def get_terrain_visualize_service() -> TerrainVisualizeService:
    return TerrainVisualizeService()

TerrainVisualizeServiceDep = Annotated[TerrainVisualizeService, Depends(get_terrain_visualize_service)]
