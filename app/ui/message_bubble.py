from nicegui import ui

from db.models.message import Message


class MessageBubble:
    """Renders a single chat message bubble.

    Layout matches the Figma reference: Morse messages align left with a
    grey bubble; plain text aligns right with a blue bubble.
    """

    def __init__(self, message: Message) -> None:
        self.message = message
        self._render()

    def _render(self) -> None:
        msg = self.message
        if msg.is_error:
            row_align = "left"
            bubble_class = "bubble bubble-error"
        elif msg.is_morse:
            row_align = "left"
            bubble_class = "bubble bubble-morse"
        else:
            row_align = "right"
            bubble_class = "bubble bubble-text"

        with ui.element("div").classes(f"bubble-row {row_align}"):
            with ui.element("div").classes(bubble_class):
                label = "Fehler" if msg.is_error else (
                    "Morse-Code" if msg.is_morse else "Text"
                )
                ui.label(label).classes("bubble-label")
                content_class = "bubble-content morse" if msg.is_morse else "bubble-content"
                ui.label(msg.content).classes(content_class)
