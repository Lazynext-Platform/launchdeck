import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, SessionLocal
from app.models.subscription import Subscription

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    db.close()

def test_create_subscription(client, db):
    subscription = {"plan_id": "price_123"}
    response = client.post("/subscriptions/", json=subscription)
    assert response.status_code == 200
    assert response.json()["plan_id"] == subscription["plan_id"]

def test_update_subscription(client, db):
    subscription = {"plan_id": "price_123"}
    response = client.post("/subscriptions/", json=subscription)
    subscription_id = response.json()["id"]
    updated_subscription = {"plan_id": "price_456"}
    response = client.put(f"/subscriptions/{subscription_id}", json=updated_subscription)
    assert response.status_code == 200
    assert response.json()["plan_id"] == updated_subscription["plan_id"]

def test_cancel_subscription(client, db):
    subscription = {"plan_id": "price_123"}
    response = client.post("/subscriptions/", json=subscription)
    subscription_id = response.json()["id"]
    response = client.delete(f"/subscriptions/{subscription_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "inactive"