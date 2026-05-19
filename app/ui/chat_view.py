"""Chat view component for message display and input."""

from datetime import datetime

from db.models import Chat
from nicegui import ui
from services import ChatService, MorseConverter
from services.file_upload_service import (
<<<<<<< Updated upstream
    EmptyFileError,
    FileEncodingError,
    FileReadError,
    FileUploadService,
=======
    FileUploadService,
    InvalidFileFormatError,
    EmptyFileError,
    MixedContentError,
>>>>>>> Stashed changes
    InvalidCharactersError,
    InvalidFileFormatError,
    InvalidMorseError,
    MixedContentError,
)

from .message_bubble import MessageBubble


class ChatView:
    """Main chat area: header, messages, input bar."""

    def __init__(self, service: ChatService, chat: Chat | None) -> None:
        self.service = service
        self.chat = chat
        self.input_value = ""
        self._render()

    def _render(self) -> None:
        with ui.element("section").classes("main-content"):
            self._render_header()
            self._render_messages()
            self._render_input_bar()

    def _render_header(self) -> None:
        with ui.element("div").classes("chat-header"):
            with ui.element("div"):
                ui.html("<h1>Morse-Code Konverter</h1>")
                ui.html(
                    "<p>Text automatisch in Morse-Code umwandeln "
                    "und umgekehrt</p>"
                )
            with ui.row().classes("items-center gap-2"):
                ui.button(
                    "Zeichentabelle",
                    icon="grid_on",
                    on_click=self._show_reference,
                ).props("flat no-caps").classes("toolbar-btn")
                if self.chat is not None and self.chat.messages:
                    ui.button(
                        "Export", icon="download", on_click=self._export_chat
                    ).props("flat no-caps").classes("toolbar-btn")

    def _render_messages(self) -> None:
        with ui.element("div").classes("messages-area"):
            if self.chat is None or not self.chat.messages:
                self._render_welcome()
                return
            with ui.element("div").classes("messages-inner"):
                for i, msg in enumerate(self.chat.messages):
                    MessageBubble(msg, is_user=(i % 2 == 0))

    def _render_welcome(self) -> None:
        with (
            ui.element("div").classes("welcome-wrap"),
            ui.element("div").classes("welcome-card"),
        ):
            ui.html("<div class='welcome-sos'>• • • − − − • • •</div>")
            ui.html(
                "<h2 class='welcome-title'>"
                "Willkommen beim Morse-Code Konverter"
                "</h2>"
            )
            ui.html(
                "<p class='welcome-text'>"
                "Geben Sie Text oder Morse-Code ein, "
                "um eine Konvertierung zu starten.</p>"
            )
            ui.html(
                "<div class='welcome-hint'>"
                "<p>• Punkt und − Strich für Morse-Code</p>"
                "<p>• Leerzeichen zwischen Zeichen</p>"
                "<p>• / für Wortabstand</p>"
                "</div>"
            )

    def _render_input_bar(self) -> None:
        with (
            ui.element("div").classes("input-bar"),
            ui.element("div").classes("input-inner"),
        ):
            ui.upload(
                label="",
                auto_upload=True,
                max_file_size=FileUploadService.MAX_FILE_SIZE_BYTES,
                on_upload=self._handle_upload,
                on_rejected=self._handle_upload_rejected,
            ).props('accept=".txt" flat dense').classes("attach-btn").tooltip(
                "Textdatei hochladen (.txt, max. "
                f"{FileUploadService.MAX_FILE_SIZE_KILOBYTES} KB)"
            )

            self.input_box = (
                ui.input(placeholder="Text oder Morse-Code eingeben…")
                .props("borderless dense")
                .classes("chat-input flex-1")
                .on("keydown.enter", self._on_send)
            )
            self.input_box.bind_value(self, "input_value")

            ui.button("Senden", icon="send", on_click=self._on_send).props(
                "unelevated no-caps"
            ).classes("send-btn")

    def _on_send(self) -> None:
        value = (self.input_value or "").strip()
        if not value:
            return
        self._send(value)

    def _send(self, value: str) -> None:
        chat_id = self.chat.id if self.chat is not None else None
        if chat_id is None:
            new_chat = self.service.create_chat()
            chat_id = new_chat.id

        try:
            self.service.send_message(chat_id, value)
        except Exception as exc:
            ui.notify(f"Fehler: {exc}", type="negative")
            return

        ui.navigate.to(f"/chat/{chat_id}")

    def _export_chat(self) -> None:
        if self.chat is None:
            return
        payload = self.service.export_chat_json(self.chat.id)
        if payload is None:
            ui.notify("Kein Inhalt zum Exportieren", type="warning")
            return
        filename = (
            f"chat_{self.chat.id}_{datetime.now().strftime('%Y-%m-%d')}.json"
        )
        ui.download(payload.encode("utf-8"), filename)

    def _handle_upload_rejected(self, event) -> None:
        ui.notify(
            "Datei ist zu groß. Maximal "
            f"{FileUploadService.MAX_FILE_SIZE_KILOBYTES} KB erlaubt.",
            type="warning",
        )

    async def _handle_upload(self, event) -> None:
        upload = getattr(event, "file", None)
        if upload is None:
            ui.notify("Datei konnte nicht gelesen werden.", type="negative")
            return

        try:
            raw_text = await upload.text(encoding="utf-8")
        except UnicodeDecodeError:
            ui.notify("Datei ist keine gültige UTF-8 Textdatei.", type="negative")
            return
        except Exception:
            ui.notify("Datei konnte nicht gelesen werden.", type="negative")
            return

<<<<<<< Updated upstream
            # Validate content (mixed content, invalid characters, etc.)
=======
        try:
            content = FileUploadService.process_upload(
                upload.name, upload.content_type, raw_text
            )
>>>>>>> Stashed changes
            content = FileUploadService.validate_content(content)
            self._send(content)

        except InvalidFileFormatError as exc:
            ui.notify(str(exc), type="warning")
        except EmptyFileError as exc:
            ui.notify(str(exc), type="warning")
        except MixedContentError as exc:
            ui.notify(str(exc), type="warning")
        except InvalidCharactersError as exc:
            ui.notify(str(exc), type="negative")
        except InvalidMorseError as exc:
            ui.notify(str(exc), type="negative")

    def _show_reference(self) -> None:
        with (
            ui.dialog().props("maximized") as dialog,
            ui.card().classes("ref-dialog"),
        ):
            ui.label("Unterstützte Zeichen").style(
                "font-size: 1.125rem; font-weight: 600;"
            )
            with ui.element("div").classes("ref-grid ref-grid--dense"):
                for char, code in MorseConverter.reference_table():
                    with ui.element("div").classes("ref-cell"):
                        ui.label(char).classes("ref-char")
                        ui.label(code).classes("ref-morse")
            with ui.row().classes("justify-end w-full ref-actions"):
                ui.button("Schließen", on_click=dialog.close).props(
                    "flat no-caps"
                )
        dialog.open()
