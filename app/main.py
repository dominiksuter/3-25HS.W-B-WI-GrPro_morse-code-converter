import os

from dotenv import load_dotenv

# Load environment variables early
load_dotenv(override=True)

from db import DatabaseManager  # noqa: E402
from ui import ViewManager  # noqa: E402

storage_secret = os.getenv(
    "SSECRET",
    "62ca79c467777fd6101172d11b555bf20608291dc0830ef9e2d66b98346372c2",
)


def start() -> None:
    """Initialize database and start the UI application."""
    DatabaseManager.init_db()
    ViewManager(storage_secret=storage_secret, show=False).run()


if __name__ in {"__main__", "__mp_main__"}:
    start()
