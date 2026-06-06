import os
from pathlib import Path

BASE_DIR=Path(__file__).resolve().parent.parent

DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite+aiosqlite:///{BASE_DIR}/adoruworld.db")

SITE_START_DATE: str = os.getenv("SITE_START_DATE", "2025-01-01")

API_PREFIX: str = "/api/v1"

PROJECT_NAME: str = "AdoruKWorld Server"
VERSION: str = "1.0.0"
DESCRIPTION: str = "AdoruKWorld personal site backend API"