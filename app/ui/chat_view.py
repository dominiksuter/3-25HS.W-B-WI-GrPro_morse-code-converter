"""Chat view component for message display and input."""

import re
from datetime import datetime

from nicegui import ui

from db.models import Chat
from services import ChatService, MorseConverter, ConversionError

from .message_bubble import MessageBubble

MAX_FILE_BYTES = 500 * 1024


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
                    "<p>Text automatisch in Morse-Code umwandeln und umgekehrt</p>"
                )
            with ui.row().classes("items-center gap-2"):
                ui.button(
                    "Zeichentabelle", icon="grid_on", on_click=self._show_reference
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
        with ui.element("div").classes("welcome-wrap"):
            with ui.element("div").classes("welcome-card"):
                ui.html("<div class='welcome-sos'>• • • − − − • • •</div>")
                ui.html("<h2 class='welcome-title'>Willkommen beim Morse-Code Konverter</h2>")
                ui.html(
                    "<p class='welcome-text'>Geben Sie Text oder Morse-Code ein, "
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
        with ui.element("div").classes("input-bar"):
            with ui.element("div").classes("input-inner"):
                ui.upload(
                    label="",
                    auto_upload=True,
                    max_file_size=MAX_FILE_BYTES,
                    on_upload=self._handle_upload,
                    on_rejected=self._handle_upload_rejected,
                ).props('accept=".txt" flat dense').classes("attach-btn").tooltip(
                    "Textdatei hochladen (.txt, max. 500 KB)"
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
            "Dateiformat nicht erlaubt. Nur .txt-Dateien möglich.",
            type="warning",
        )

    async def _handle_upload(self, event) -> None:
        upload = getattr(event, "file", None)
        filename = (getattr(upload, "name", "") or "").strip()
        content_type = (getattr(upload, "content_type", "") or "").strip().lower()

        # Enforce file type: allow only .txt; fall back to MIME type if name is missing.
        is_txt_by_name = bool(filename) and filename.lower().endswith(".txt")
        is_txt_by_mime = content_type.startswith("text/") or content_type == ""
        if not is_txt_by_name and not (not filename and is_txt_by_mime):
            ui.notify(
                "Dateiformat nicht erlaubt. Nur .txt-Dateien möglich.",
                type="warning",
            )
            return

        try:
            raw = await upload.text(encoding="utf-8")
        except UnicodeDecodeError:
            ui.notify("Datei ist keine gültige UTF-8 Textdatei.", type="negative")
            return
        except Exception:
            ui.notify("Datei konnte nicht gelesen werden.", type="negative")
            return

        # normalize whitespace (allow multi-line files)
        content = " ".join((raw or "").split()).strip()
        if not content:
            ui.notify("Datei ist leer.", type="warning")
            return

        # Decide whether the file is Morse-only or Text-only.
        is_morse_only = MorseConverter.is_morse(content)

        if is_morse_only:
            # Validate Morse tokens early so we can show a popup instead of writing an error bubble.
            try:
                MorseConverter.decode(content)
            except ConversionError as exc:
                ui.notify(str(exc), type="negative")
                return
            self._send(content)
            return

        # Reject mixed files: letters + standalone morse tokens like "..." or "-.-".
        has_letter = any(ch.isalpha() for ch in content)
        has_morse_token = re.search(r"(^|\s)[.-]{1,6}(?=\s|/|$)", content) is not None
        if has_letter and has_morse_token:
            ui.notify(
                "Datei enthält gemischten Inhalt (Text und Morse-Code). Bitte nur eines davon.",
                type="warning",
            )
            return

        # Validate allowed characters for text using the dictionary.
        invalid = sorted({ch for ch in content.upper() if ch not in MorseConverter.TO_MORSE})
        if invalid:
            preview = ", ".join(invalid[:8])
            more = " …" if len(invalid) > 8 else ""
            ui.notify(f"Ungültige Zeichen in Datei: {preview}{more}", type="negative")
            return

        self._send(content)

    def _show_reference(self) -> None:
        with ui.dialog().props("maximized") as dialog, ui.card().classes("ref-dialog"):
            ui.label("Unterstützte Zeichen").style(
                "font-size: 1.125rem; font-weight: 600;"
            )
            with ui.element("div").classes("ref-grid ref-grid--dense"):
                for char, code in MorseConverter.reference_table():
                    with ui.element("div").classes("ref-cell"):
                        ui.label(char).classes("ref-char")
                        ui.label(code).classes("ref-morse")
            with ui.row().classes("justify-end w-full ref-actions"):
                ui.button("Schließen", on_click=dialog.close).props("flat no-caps")
        dialog.open()
