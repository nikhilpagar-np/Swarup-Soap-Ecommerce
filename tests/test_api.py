import os
os.environ["DATABASE_URL"] = "sqlite:///./data/test-swarupsoap.db"

from fastapi.testclient import TestClient
from app.main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_catalog_contains_confirmed_variants():
    with TestClient(app) as client:
        response = client.get("/api/products")
        assert response.status_code == 200
        variants = response.json()[0]["variants"]
        skus = {item["sku"] for item in variants}
        assert "SWARUP-15-SINGLE" in skus
        assert "SWARUP-20-PACK10" not in {item["sku"] for item in variants if item["is_active"]}


def test_missing_product():
    with TestClient(app) as client:
        assert client.get("/api/products/99999").status_code == 404
