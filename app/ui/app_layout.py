from nicegui import ui

from app.services.chat_service import ChatService
from app.ui.chat_view import ChatView
from app.ui.sidebar import Sidebar
from app.ui.styles import CUSTOM_CSS


def render_layout(chat_id: int | None) -> None:
    """Render the full app shell (sidebar + content) for a given chat id."""
    ui.add_head_html(CUSTOM_CSS)
    service = ChatService()

    chat = service.get_chat(chat_id) if chat_id is not None else None
    active_id = chat.id if chat is not None else None

    if chat_id is not None and chat is None:
        ui.navigate.to("/")
        return

    with ui.element("div").classes("app-shell"):
        Sidebar(service, active_id)
        ChatView(service, chat)


def register_pages() -> None:
    @ui.page("/")
    def index_page():
        render_layout(None)

    @ui.page("/chat/{chat_id}")
    def chat_page(chat_id: int):
        render_layout(chat_id)
