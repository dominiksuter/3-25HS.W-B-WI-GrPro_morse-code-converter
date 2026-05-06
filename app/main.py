from nicegui import ui

from dotenv import load_dotenv

from db.database_manager import DatabaseManager
from ui.app_layout import register_pages

load_dotenv()


def start() -> None:
    DatabaseManager.init_db()
    register_pages()
    ui.run(
        title="Morse-Code Konverter",
        host="localhost",
        port=8080,
        reload=False,
        show=False,
    )


if __name__ in {"__main__", "__mp_main__"}:
    start()
