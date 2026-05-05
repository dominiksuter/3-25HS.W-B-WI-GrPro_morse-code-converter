from nicegui import ui

from app.services.chat_service import ChatService


class Sidebar:
    """Left navigation sidebar listing all chats."""

    def __init__(self, service: ChatService, active_chat_id: int | None) -> None:
        self.service = service
        self.active_chat_id = active_chat_id
        self._render()

    def _render(self) -> None:
        with ui.element("aside").classes("sidebar"):
            with ui.element("div").classes("sidebar-header"):
                ui.button(
                    "Neuer Chat",
                    icon="add_circle_outline",
                    on_click=self._new_chat,
                ).props("unelevated no-caps").classes("sidebar-new-btn")

            with ui.element("div").classes("sidebar-list"):
                chats = self.service.list_chats()
                if not chats:
                    ui.label("Keine Chats vorhanden").classes("sidebar-empty")
                else:
                    for chat in chats:
                        self._render_chat_row(chat)

            with ui.element("div").classes("sidebar-footer"):
                ui.label("Text ↔ Morse-Code")
                ui.label("Konverter mit Chat-Historie")

    def _render_chat_row(self, chat) -> None:
        is_active = chat.id == self.active_chat_id
        row_class = "chat-row active" if is_active else "chat-row"
        with ui.element("div").classes(row_class).on(
            "click", lambda c=chat: ui.navigate.to(f"/chat/{c.id}")
        ):
            ui.icon("chat_bubble_outline").style("font-size: 16px;")
            ui.label(chat.title).classes("title")
            pin_icon = "push_pin" if chat.pinned else "o_push_pin"
            ui.button(
                icon=pin_icon,
                on_click=lambda c=chat: self._toggle_pin(c.id),
            ).props("flat dense round").classes(
                "icon-btn pin-btn" + (" pinned" if chat.pinned else "")
            )
            with ui.element("div").classes("actions"):
                ui.button(
                    icon="delete_outline",
                    on_click=lambda c=chat: self._delete_chat(c.id),
                ).props("flat dense round").classes("icon-btn")

    def _new_chat(self) -> None:
        chat = self.service.create_chat()
        ui.navigate.to(f"/chat/{chat.id}")

    def _toggle_pin(self, chat_id: int) -> None:
        self.service.toggle_pin(chat_id)
        ui.navigate.to(f"/chat/{chat_id}" if chat_id == self.active_chat_id else "/")

    def _delete_chat(self, chat_id: int) -> None:
        self.service.delete_chat(chat_id)
        if chat_id == self.active_chat_id:
            ui.navigate.to("/")
        else:
            ui.navigate.to(
                f"/chat/{self.active_chat_id}" if self.active_chat_id else "/"
            )
