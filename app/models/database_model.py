from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.orm import relationship

from app.database.database_setup import Base


class BuildingLimit(Base):
    __tablename__ = "building_limits"

    id = Column(Integer, primary_key=True, index=True)
    geometry = Column(String)
    version = Column(Integer, default=1)

    split_building_limits = relationship("SplitBuildingLimit", back_populates="building_limit")

class HeightPlateau(Base):
    __tablename__ = "height_plateaus"

    id = Column(Integer, primary_key=True, index=True)
    geometry = Column(String)
    elevation = Column(Float)
    version = Column(Integer, default=1)

    split_building_limits = relationship("SplitBuildingLimit", back_populates="height_plateau")

class SplitBuildingLimit(Base):
    __tablename__ = "split_building_limits"

    id = Column(Integer, primary_key=True, index=True)
    geometry = Column(String)
    elevation = Column(Float)
    version = Column(Integer, default=1)

    building_limit_id = Column(Integer, ForeignKey('building_limits.id'))
    height_plateau_id = Column(Integer, ForeignKey('height_plateaus.id'))
    building_limit = relationship("BuildingLimit", back_populates="split_building_limits")
    height_plateau = relationship("HeightPlateau", back_populates="split_building_limits")