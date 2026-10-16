"""Application settings for local SQLite and production PostgreSQL."""
from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = PROJECT_ROOT / "frontend"
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def resolve_database_url() -> str:
    configured = os.getenv("DATABASE_URL", "").strip()
    if configured.startswith("postgres://"):
        return configured.replace("postgres://", "postgresql+psycopg://", 1)
    if configured.startswith("postgresql://") or configured.startswith("postgresql+"):
        return configured
    if configured.startswith("sqlite:///"):
        return configured
    return f"sqlite:///{DATA_DIR / 'swarupsoap.db'}"


class Settings:
    app_name = "Swarup Soap E-Commerce"
    environment = os.getenv("APP_ENV", "development")
    secret_key = os.getenv("APP_SECRET_KEY", "dev-only-change-me")
    database_url = resolve_database_url()
    frontend_dir = FRONTEND_DIR
    data_dir = DATA_DIR
    razorpay_key_id = os.getenv("RAZORPAY_KEY_ID", "")
    razorpay_key_secret = os.getenv("RAZORPAY_KEY_SECRET", "")


settings = Settings()
