from sqlalchemy.orm import Session
from geopandas import GeoDataFrame

from app.models.database_model import BuildingLimit, HeightPlateau, SplitBuildingLimit

class DatabaseService:
    def __init__(self):
        pass

    async def create_building_limits(self, db: Session, building_limits_gdf: GeoDataFrame) -> list[int]:
        created_ids = []
        building_limits = []
        
        for _, building_polygon in building_limits_gdf.iterrows():
            geometry_wkt = building_polygon.geometry.wkt
            building_limit = BuildingLimit(
                geometry=geometry_wkt,
                version=1,
            )
            db.add(building_limit)
            building_limits.append(building_limit)
        db.commit()

        created_ids = [limit.id for limit in building_limits]
        return created_ids

    async def create_height_plateaus(self, db: Session, height_plateaus_gdf: GeoDataFrame) -> list[int]:
        created_ids = []
        height_plateaus = []
        
        for _, plateau_polygon in height_plateaus_gdf.iterrows():
            geometry_wkt = plateau_polygon.geometry.wkt
            height_plateau = HeightPlateau(
                geometry=geometry_wkt,
                elevation=plateau_polygon["elevation"],
                version=1,
            )
            db.add(height_plateau)
            height_plateaus.append(height_plateau)
        db.commit()

        created_ids = [plateau.id for plateau in height_plateaus]
        return created_ids

    async def create_split_building_limits(
        self, 
        db: Session, 
        split_limits_gdf: GeoDataFrame, 
        building_limit_id_list: list[int], 
        height_plateau_list: list[int]
    ) -> list[int]:
        created_ids = []
        split_building_limits = []

        for _, split_building_polygon in split_limits_gdf.iterrows():
            geometry_wkt = split_building_polygon.geometry.wkt
            building_limit_id = building_limit_id_list[split_building_polygon.building_limit_id]
            height_plateau_id = height_plateau_list[split_building_polygon.height_plateau_id]

            split_building_limit = SplitBuildingLimit(
                geometry=geometry_wkt,
                elevation=split_building_polygon.elevation,
                version=1,
                building_limit_id=building_limit_id,
                height_plateau_id=height_plateau_id,
            )
            db.add(split_building_limit)
            split_building_limits.append(split_building_limit)
        db.commit()

        created_ids = [limit.id for limit in split_building_limits]
        return created_ids