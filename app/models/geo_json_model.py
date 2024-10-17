from pydantic import BaseModel, Field
from app.models.enums import GeometryType, FeatureType, FeatureCollectionType

class _Geometry(BaseModel):
    type: GeometryType = GeometryType.POLYGON
    coordinates: list[list[list[float]]] = Field(default_factory=list)

class _Properties(BaseModel):
    elevation: float | None = None

class _Feature(BaseModel):
    type: FeatureType = FeatureType.FEATURE
    properties: _Properties = Field(default_factory=dict)
    geometry: _Geometry

class GeoJson(BaseModel):
    type: FeatureCollectionType = FeatureCollectionType.FEATURE_COLLECTION
    features: list[_Feature] = Field(default_factory=list)

class TerrainSplitRequest(BaseModel):
    building_limits: GeoJson
    height_plateaus: GeoJson

class TerrainSplitResponse(BaseModel):
    buildingLimitIds: list[int] | None = []
    heightPlateauIds: list[int] | None = []
    splitBuildingLimitIds: list[int] | None = []