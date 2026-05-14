"""Left navigation sidebar for chat management."""

from nicegui import ui

from services import ChatService


class Sidebar:
    """Left navigation sidebar listing all chats."""

    def __init__(self, service: ChatService, active_chat_id: str | None) -> None:
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
            pin_btn = ui.button(icon=pin_icon).props("flat dense round").classes(
                "icon-btn pin-btn" + (" pinned" if chat.pinned else "")
            )
            pin_btn.on(
                "click",
                lambda _e, c=chat: self._toggle_pin(c.id),
                js_handler="(e) => { e.stopPropagation(); emit(e); }",
            )
            with ui.element("div").classes("actions"):
                rename_btn = ui.button(icon="edit").props("flat dense round").classes(
                    "icon-btn"
                )
                rename_btn.on(
                    "click",
                    lambda _e, c=chat: self._rename_chat(c.id, c.title),
                    js_handler="(e) => { e.stopPropagation(); emit(e); }",
                )

                delete_btn = ui.button(icon="delete_outline").props(
                    "flat dense round"
                ).classes("icon-btn")
                delete_btn.on(
                    "click",
                    lambda _e, c=chat: self._delete_chat(c.id),
                    js_handler="(e) => { e.stopPropagation(); emit(e); }",
                )

    def _new_chat(self) -> None:
        chat = self.service.create_chat()
        ui.navigate.to(f"/chat/{chat.id}")

    def _toggle_pin(self, chat_id: str) -> None:
        self.service.toggle_pin(chat_id)
        ui.navigate.to(f"/chat/{chat_id}" if chat_id == self.active_chat_id else "/")

    def _rename_chat(self, chat_id: str, current_title: str) -> None:
        with ui.dialog() as dialog, ui.card().style("min-width: 420px;"):
            ui.label("Chat umbenennen").style("font-size: 1.05rem; font-weight: 600;")
            title_input = ui.input(value=current_title, placeholder="Name eingeben …").props(
                "autofocus"
            )
            with ui.row().classes("justify-end w-full"):
                ui.button("Abbrechen", on_click=dialog.close).props("flat no-caps")

                def save() -> None:
                    self.service.rename_chat(chat_id, title_input.value)
                    dialog.close()
                    ui.navigate.to(
                        f"/chat/{self.active_chat_id}" if self.active_chat_id else "/"
                    )

                ui.button("Speichern", on_click=save).props("unelevated no-caps")
        dialog.open()

    def _delete_chat(self, chat_id: str) -> None:
        self.service.delete_chat(chat_id)
        if chat_id == self.active_chat_id:
            ui.navigate.to("/")
        else:
            ui.navigate.to(
                f"/chat/{self.active_chat_id}" if self.active_chat_id else "/"
            )
