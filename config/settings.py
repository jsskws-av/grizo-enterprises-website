"""
Application Settings and Environment Configuration
"""

import os
from pathlib import Path
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "ecommerce_system.db"
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"
SYNC_DATABASE_URL = f"sqlite:///{DB_PATH}"


class Settings(BaseModel):
    app_name: str = "AI E-Commerce Research & Management System"
    app_version: str = "1.0.0"
    environment: str = os.getenv("ENVIRONMENT", "development")
    secret_key: str = os.getenv("SECRET_KEY", "prod-in-secret-ecom-agentic-key-2026")
    default_currency: str = "INR"
    default_timezone: str = "Asia/Kolkata"
    default_marketplace_id: str = "A21TJRUUN4KGV"  # Amazon.in
    
    # Credential vault master key (32 bytes base64 for Fernet)
    vault_master_key: str = os.getenv(
        "VAULT_MASTER_KEY",
        "dGVzdC12YXVsdC1rZXktZm9yLWFtYXpvbi1pbi1lY29tLTEyMw=="
    )
    
    # AI Engine
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = "gemini-2.5-flash"
    
    # Notification Integrations
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")
    smtp_host: str = os.getenv("SMTP_HOST", "")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: str = os.getenv("SMTP_USER", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    alert_recipient_email: str = os.getenv("ALERT_RECIPIENT_EMAIL", "")

    # Scheduler config (IST times)
    morning_sync_hour: int = 7
    morning_sync_minute: int = 30
    midday_monitor_hour: int = 13
    midday_monitor_minute: int = 0
    evening_report_hour: int = 20
    evening_report_minute: int = 0


settings = Settings()
