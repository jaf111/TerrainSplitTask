from unittest import TestCase
from unittest.mock import MagicMock
from geopandas import GeoDataFrame
from pytest import raises
from shapely import LineString
from shapely.geometry import Polygon

from app.models.exception_model import UncoveredAreaException, UnexpectedGeometryException
from app.services.terrain_service import TerrainService


class TestTerrainService(TestCase):
    def setUp(self):
        self.mock_db_service = MagicMock()
        self.terrain_service = TerrainService(database_service=self.mock_db_service)

    def test_split_building_limits_with_full_cover(self):
        building_limits_gdf = GeoDataFrame({
        'geometry': [Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])]
        })

        height_plateaus_gdf = GeoDataFrame({
            'geometry': [Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])],
            'elevation': [10]
        })

        result = self.terrain_service.split_building_limits(building_limits_gdf, height_plateaus_gdf)

        assert len(result) == 1
        assert 'elevation' in result.columns
        assert result['elevation'].iloc[0] == 10
    
    def test_split_building_limits_no_intersection(self):
        building_limits_gdf = GeoDataFrame({
            'geometry': []
        })
        height_plateaus_gdf = GeoDataFrame({
            'geometry': [Polygon([(2, 2), (3, 2), (3, 3), (2, 3)])],
            'elevation': [10]
        })

        result = self.terrain_service.split_building_limits(building_limits_gdf, height_plateaus_gdf)

        assert result.empty

    def test_split_building_limits_with_problematic_plateau(self):
        building_limits_gdf = GeoDataFrame({
            'geometry': [Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])],
        })

        plateau_polygon = Polygon([(0, 0), (3, 0), (3, 3), (0, 3), (0, 0)])
        problematic_plateau = LineString([(2, 0), (2, 2)])
        height_plateaus_gdf = GeoDataFrame(
            [
                {'geometry': plateau_polygon, 'elevation': 10},
                {'geometry': problematic_plateau, 'elevation': 15}
            ],
        )

        with raises(UnexpectedGeometryException):
            self.terrain_service.split_building_limits(building_limits_gdf, height_plateaus_gdf)

    def test_split_building_limits_with_buffer(self):
        buffer_threshold = 0.001

        building_limits_gdf = GeoDataFrame({
            'geometry': [Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])]
        })
        height_plateaus_gdf = GeoDataFrame({
            'geometry': [Polygon([(0, 0), (1-buffer_threshold, 0), (1, 1), (0, 1)])],
            'elevation': [10]
        })

        result = self.terrain_service.split_building_limits(building_limits_gdf, height_plateaus_gdf)

        assert len(result) == 1
        assert 'elevation' in result.columns
        assert result['elevation'].iloc[0] == 10

    def test_split_building_limits_with_too_large_buffer(self):
        buffer_threshold = 0.002

        building_limits_gdf = GeoDataFrame({
            'geometry': [Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])]
        })
        height_plateaus_gdf = GeoDataFrame({
            'geometry': [Polygon([(0, 0), (1-buffer_threshold, 0), (1, 1), (0, 1)])],
            'elevation': [10]
        })

        with raises(UncoveredAreaException):
            self.terrain_service.split_building_limits(building_limits_gdf, height_plateaus_gdf)

    def test_split_building_limits_with_large_uncovered_gap(self):
        building_limits_gdf = GeoDataFrame({
            'geometry': [Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])]
        })
        height_plateaus_gdf = GeoDataFrame({
            'geometry': [Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])],
            'elevation': [10]
        })

        with raises(UncoveredAreaException):
            self.terrain_service.split_building_limits(building_limits_gdf, height_plateaus_gdf)