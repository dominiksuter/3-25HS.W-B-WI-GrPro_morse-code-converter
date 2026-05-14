from nicegui import ui

from db.models import Message


class MessageBubble:

    def __init__(self, message: Message, is_user: bool = False) -> None:
        self.message = message
        self.is_user = is_user
        self._render()

    def _render(self) -> None:
        msg = self.message
        if msg.is_error:
            row_align = "left"
            bubble_class = "bubble bubble-error"
        elif self.is_user:
            row_align = "right"
            bubble_class = "bubble bubble-text"
        else:
            row_align = "left"
            bubble_class = "bubble bubble-morse"

        with ui.element("div").classes(f"bubble-row {row_align}"):
            with ui.element("div").classes(bubble_class):
                label = "Fehler" if msg.is_error else (
                    "Morse-Code" if msg.is_morse else "Text"
                )
                ui.label(label).classes("bubble-label")
                content_class = "bubble-content morse" if msg.is_morse else "bubble-content"
                ui.label(msg.content).classes(content_class)
