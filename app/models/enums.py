from enum import Enum


class GeometryType(str, Enum):
    POLYGON = "Polygon"

class FeatureType(str, Enum):
    FEATURE = "Feature"

class FeatureCollectionType(str, Enum):
    FEATURE_COLLECTION = "FeatureCollection"

class ErrorCodes(str, Enum):
    UNCOVERED_AREA_ERROR = "uncovered_area_error"
    GEOMETRY_ERROR = "geometry_error"
    SYSTEM_ERROR = "system_error"