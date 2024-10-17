from matplotlib.pyplot import grid, show, subplots
from fastapi.encoders import jsonable_encoder
from geopandas import GeoDataFrame

from app.models.geo_json_model import GeoJson


class TerrainVisualizeService:
    def __init__(self):
        pass

    def visualize_terrain(self, building_limits: GeoJson, height_plateaus: GeoJson) -> None:
        building_limits_json = jsonable_encoder(building_limits)
        height_plateaus_json = jsonable_encoder(height_plateaus)
        building_limits_gdf = GeoDataFrame.from_features(building_limits_json["features"])
        height_plateaus_gdf = GeoDataFrame.from_features(height_plateaus_json['features'])

        _, ax = subplots(figsize=(10, 10))
        building_limits_gdf.plot(ax=ax, color='blue', edgecolor='black', label='Building Limits')
        height_plateaus_gdf.plot(ax=ax, color='red', edgecolor='green', alpha=0.5, label='Height Plateaus')

        ax.set_title('Building Limits and Height Plateaus Visualization')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')

        grid()
        show()
