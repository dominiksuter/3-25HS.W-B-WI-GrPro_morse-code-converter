from nicegui import ui

from app.database import init_db
from app.ui.app_layout import register_pages


def start() -> None:
    init_db()
    register_pages()
    ui.run(title="Morse-Code Konverter", port=8080, reload=False, show=False)


if __name__ in {"__main__", "__mp_main__"}:
    start()
