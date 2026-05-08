from dotenv import load_dotenv

load_dotenv(override=True)

import os
from pathlib import Path
from nicegui import ui
from db.database_manager import DatabaseManager
from ui.app_layout import register_pages


storage_secret = os.getenv(
    "SSECRET",
    "62ca79c467777fd6101172d11b555bf20608291dc0830ef9e2d66b98346372c2",
)

FAVICON = Path(__file__).parent / "ui" / "favicon.png"


def start() -> None:
    DatabaseManager.init_db()
    register_pages()
    ui.run(
        title="Morse-Code Konverter",
        host="localhost",
        port=8080,
        reload=False,
        storage_secret=storage_secret,
        favicon=str(FAVICON),
    )


if __name__ in {"__main__", "__mp_main__"}:
    start()
