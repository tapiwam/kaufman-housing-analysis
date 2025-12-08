"""Configuration settings for the CAD data loader application."""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "Kaufman-CAD-2025-Certified-Full-Roll-Download-updated-with-Supp-5"
CONFIG_DIR = BASE_DIR / "config"

# Database settings
DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "kaufman_cad"),
    "user": os.getenv("DB_USER", "cad_user"),
    "password": os.getenv("DB_PASSWORD", "cad_password"),
    "schema": os.getenv("DB_SCHEMA", "cad"),
}

# File settings
FILE_ENCODING = "utf-8"
FILE_PREFIX = "2025-10-27_002174_APPRAISAL_"

# Processing settings
BATCH_SIZE = 1000  # Records per batch for database inserts
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
