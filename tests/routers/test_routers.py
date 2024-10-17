from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database_setup import get_db
from app.models.geo_json_model import TerrainSplitResponse
from app.database.database_setup import Base
from app.main import app

from tests.test_data import test_data_for_terrain_split


test_engine = create_engine(
    "sqlite:///./test.db", connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base.metadata.create_all(bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_split_terrain_router():
    post_body = test_data_for_terrain_split
    response = client.post("/terrain/split", json=post_body)

    assert response.status_code == 201
    response_model = TerrainSplitResponse(**response.json())
    assert len(response_model.buildingLimitIds) == 1
    assert len(response_model.heightPlateauIds) == 3
    assert len(response_model.splitBuildingLimitIds) == 3

    Base.metadata.drop_all(test_engine)
