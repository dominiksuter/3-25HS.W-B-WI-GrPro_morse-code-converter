from nicegui import ui, app as nicegui_app
import uuid
from services import ChatService
from ui.chat_view import ChatView
from ui.sidebar import Sidebar
from ui.styles import CUSTOM_CSS


def _ensure_session_auid() -> str:
    # Anonymous user id persisted in NiceGUI session storage.
    if "auid" not in nicegui_app.storage.user:
        nicegui_app.storage.user["auid"] = str(uuid.uuid4())
    return str(nicegui_app.storage.user["auid"])


def render_layout(chat_id: str | None, auid: str) -> None:
    """Render the full app shell (sidebar + content) for a given chat id."""
    ui.add_head_html(CUSTOM_CSS)
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
    @ui.page("/")
    def index_page():
        auid = _ensure_session_auid()
        render_layout(None, auid)

    @ui.page("/chat/{chat_id}")
    def chat_page(chat_id: str):
        auid = _ensure_session_auid()
        render_layout(chat_id, auid)
