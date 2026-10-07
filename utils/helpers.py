import os
from datetime import datetime


def format_date(parsed) -> str:
    """struct_time -> '06 Oct 2026'; tolerant of missing values."""
    try:
        return datetime(*parsed[:6]).strftime("%d %b %Y")
    except Exception:
        return "Date unavailable"


def get_secret(name: str, secrets) -> str | None:
    """st.secrets first, then environment variable."""
    try:
        v = secrets.get(name)
        if v:
            return v
    except Exception:
        pass
    return os.environ.get(name) or None


def get_api_key(sidebar_value: str, secrets) -> str | None:
    """Priority: sidebar input > st.secrets > environment variable."""
    return sidebar_value or get_secret("GOOGLE_PLACES_API_KEY", secrets)
