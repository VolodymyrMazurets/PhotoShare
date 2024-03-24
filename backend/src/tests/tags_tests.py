from fastapi.testclient import TestClient
from src.core.db import SessionLocal, engine, get_db
from src.models import Tag
from src.main import app


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_add_tags_to_image():
    response = client.post("/images/1/tags/", json={"tags": ["tag1", "tag2", "tag3"]}, headers={"X-Access-Token": "token"})
    assert response.status_code == 200
    assert response.json() == {"tags": ["tag1", "tag2", "tag3"]}

    with SessionLocal() as db:
        assert db.query(Tag).filter(Tag.name.in_(["tag1", "tag2", "tag3"])).count() == 3

    response = client.post("/images/1/tags/", json={"tags": ["tag4", "tag5"]}, headers={"X-Access-Token": "token"})
    assert response.status_code == 200
    assert response.json() == {"tags": ["tag4", "tag5"]}

    with SessionLocal() as db:
        assert db.query(Tag).filter(Tag.name.in_(["tag4", "tag5"])).count() == 2

    response = client.post("/images/1/tags/", json={"tags": ["tag1", "tag2"]}, headers={"X-Access-Token": "token"})
    assert response.status_code == 200
    assert response.json() == {"tags": ["tag1", "tag2"]}
