import logging
from sqlalchemy.orm import Session
from shapely import MultiPolygon, Polygon, unary_union
from fastapi.encoders import jsonable_encoder
from geopandas import GeoDataFrame

from app.database.database_service import DatabaseService
from app.models.exception_model import UncoveredAreaException, UnexpectedGeometryException
from app.models.geo_json_model import GeoJson, TerrainSplitResponse

logger = logging.getLogger(__name__)

class TerrainService:
    def __init__(self, database_service: DatabaseService):
        self.db_service = database_service

    def process_geo_json(self, geo_json_model: GeoJson) -> GeoDataFrame:
        geo_json = jsonable_encoder(geo_json_model)
        return GeoDataFrame.from_features(geo_json["features"])

    def split_building_limits(self, building_limits_gdf: GeoDataFrame, height_plateaus_gdf: GeoDataFrame) -> GeoDataFrame:
        split_limits = []
        combined_plateaus = unary_union(height_plateaus_gdf.geometry)
        for building_limit_index, limit in building_limits_gdf.iterrows():
            building_polygon = limit.geometry

            self._validate_and_adjust_building_plateaus_cover_building_limits(combined_plateaus, building_polygon)

            for plateau_index, plateau in height_plateaus_gdf.iterrows():
                plateau_polygon = plateau.geometry
                if building_polygon.intersects(plateau_polygon):
                    intersection = building_polygon.intersection(plateau_polygon)
                    if isinstance(intersection, Polygon):
                        split_limits.append({
                            'geometry': intersection,
                            'elevation': plateau.elevation,
                            'building_limit_id': building_limit_index,
                            'height_plateau_id': plateau_index
                        })
                    else:
                        logger.warning(f"Unexpected geometry type in intersection: {type(intersection)}")
                        raise UnexpectedGeometryException(status_code=400, intersection=intersection)
        if split_limits:
            return GeoDataFrame(split_limits, crs=building_limits_gdf.crs)
        else:
            logger.info("no split building limits were found")
            return GeoDataFrame(columns=["geometry", "elevation"], crs=building_limits_gdf.crs)

    def _validate_and_adjust_building_plateaus_cover_building_limits(self, combined_plateaus: Polygon | MultiPolygon, building_polygon: Polygon) -> bool:
        if not combined_plateaus.covers(building_polygon):
            uncovered_area = building_polygon.difference(combined_plateaus)
            if not uncovered_area.is_empty:
                logger.warning(f"Uncovered area detected in building limits: {uncovered_area}")
                return self._try_to_fill_in_gaps_with_buffer(uncovered_area, combined_plateaus, building_polygon)
        return True

    def _try_to_fill_in_gaps_with_buffer(
        self, 
        uncovered_area: Polygon, 
        combined_plateaus: Polygon | MultiPolygon, 
        building_polygon: Polygon, 
        buffer_threshold: float = 0.001
    ) -> bool:
        if uncovered_area.area <= buffer_threshold:
            buffered_plateaus = combined_plateaus.buffer(buffer_threshold)
            if buffered_plateaus.covers(building_polygon):
                logger.info("Small gaps were filled using a buffer.")
                return True
            else:
                logger.warning(f"Even after buffering, the building limits are not fully covered.")
                raise UncoveredAreaException(status_code=400, uncovered_area=uncovered_area)
        else:
            logger.warning(f"Uncovered area detected in building limits: {uncovered_area}")
            raise UncoveredAreaException(status_code=400, uncovered_area=uncovered_area)

    async def terrain_create(
        self, 
        db: Session, 
        building_limits_gdf: GeoDataFrame, 
        height_plateaus_gdf: GeoDataFrame, 
        split_limits: GeoDataFrame
    ) -> TerrainSplitResponse:
        building_limit_id_list = await self.db_service.create_building_limits(db, building_limits_gdf)
        height_plateau_list = await self.db_service.create_height_plateaus(db, height_plateaus_gdf)
        split_building_limit_list = await self.db_service.create_split_building_limits(db, split_limits, building_limit_id_list, height_plateau_list)
        return TerrainSplitResponse(
            buildingLimitIds=building_limit_id_list, 
            heightPlateauIds=height_plateau_list, 
            splitBuildingLimitIds=split_building_limit_list
        )
