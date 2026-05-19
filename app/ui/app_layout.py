"""Page registration and layout rendering."""

from nicegui import ui
from services import ChatService, UserManager

from .chat_view import ChatView
from .sidebar import Sidebar


def render_layout(chat_id: str | None) -> None:
    """Render the full app shell (sidebar + content) for a given chat id."""
    auid = UserManager.anonymous_session_user()
    service = ChatService(auid)

    chat = service.get_chat(chat_id) if chat_id is not None else None
    active_id = chat.id if chat is not None else None

    if chat_id is not None and chat is None:
        ui.navigate.to("/")
        return

    with ui.element("div").classes("app-shell"):
        Sidebar(service, active_id)
        ChatView(service, chat)


def register_pages() -> None:
    """Register all application routes."""

    @ui.page("/")
    def index_page():
        render_layout(None)

    @ui.page("/chat/{chat_id}")
    def chat_page(chat_id: str):
        render_layout(chat_id)
