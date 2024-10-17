from fastapi import APIRouter
from pathlib import Path

from app.dependencies.services_dependency import TerrainServiceDep, TerrainVisualizeServiceDep
from app.database.database_setup import SQliteDep
from app.models.geo_json_model import TerrainSplitRequest, TerrainSplitResponse
from app.models.error_model import error_responses_400, error_responses_500


router = APIRouter()

@router.post(
    "/split", 
    response_model=TerrainSplitResponse, 
    status_code=201,
    summary = 'Splitting up the building limits according to the height plateaus and stores building limits, height plateaus and split building limits.',
    description=Path('app/routers/api_docs/terrain_split.md').read_text(), 
    responses={**error_responses_400, **error_responses_500},
)
async def split_polygons(terrain_split_request: TerrainSplitRequest, terrain_service: TerrainServiceDep, db: SQliteDep) -> TerrainSplitResponse:
    building_limits = terrain_service.process_geo_json(terrain_split_request.building_limits)
    height_plateaus = terrain_service.process_geo_json(terrain_split_request.height_plateaus)
    split_limits = terrain_service.split_building_limits(building_limits, height_plateaus) 
    terrain_split_response = await terrain_service.terrain_create(db, building_limits, height_plateaus, split_limits)
    return terrain_split_response


@router.post(
    "/visualize",
    response_model=None, 
    status_code=200,
    summary = 'Only for visualization and understanding of task.',
    description="Visualize ugly plot of building limits and height plateaus. Use same post body as terrain split",
    responses={**error_responses_500}, 
)
async def visualize_terrain(terrain_split_request: TerrainSplitRequest, terrain_visualize_service: TerrainVisualizeServiceDep):
    terrain_visualize_service.visualize_terrain(terrain_split_request.building_limits, terrain_split_request.height_plateaus)
