import json
from datetime import datetime

from nicegui import ui

from main import TO_MORSE_DICT, TO_TEXT_DICT, HISTORY_FILE, save_to_json

# ---------------------------------------------------------------------------
# Morse encode / decode (GUI versions without print_error side-effects)
# ---------------------------------------------------------------------------


def encode_gui(text: str) -> tuple[str | None, str | None]:
    text = text.upper()
    encoded = []
    for ch in text:
        if ch in TO_MORSE_DICT:
            encoded.append(TO_MORSE_DICT[ch])
        else:
            return None, f"'{ch}' kann nicht in Morse-Code dargestellt werden!"
    result = " ".join(encoded)
    save_to_json(text, result)
    return result, None


def decode_gui(morse: str) -> tuple[str | None, str | None]:
    words = morse.strip().split(" ")
    decoded = []
    for code in words:
        if code in TO_TEXT_DICT:
            decoded.append(TO_TEXT_DICT[code])
        else:
            return None, f"'{code}' ist kein gültiger Morse-Buchstabe!"
    result = "".join(decoded)
    save_to_json(morse, result)
    return result, None


# ---------------------------------------------------------------------------
# History helpers
# ---------------------------------------------------------------------------


def load_history() -> list[dict]:
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def clear_history_file():
    HISTORY_FILE.write_text("[]", encoding="utf-8")


# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

body {
    background: #0f172a !important;
    min-height: 100vh;
    font-family: 'Inter', sans-serif !important;
}
.nicegui-content {
    background: transparent !important;
}

/* Main container */
.main-container {
    max-width: 900px;
    margin: 0 auto;
}

/* Hero section */
.hero-title {
    font-family: 'Inter', sans-serif !important;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #06b6d4, #8b5cf6, #ec4899) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}
.hero-subtitle {
    color: #94a3b8 !important;
    font-size: 1rem !important;
    font-weight: 400 !important;
}

/* Cards */
.converter-card {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 20px !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}
.converter-card:hover {
    border-color: #475569 !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
}

/* Section headers */
.section-label {
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #64748b !important;
}
.section-title {
    font-size: 1.25rem !important;
    font-weight: 600 !important;
    color: #f1f5f9 !important;
}

/* Morse output */
.morse-output {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.1em !important;
    letter-spacing: 3px !important;
    color: #06b6d4 !important;
}

/* Result cards */
.result-card {
    background: rgba(6, 182, 212, 0.08) !important;
    border: 1px solid rgba(6, 182, 212, 0.2) !important;
    border-radius: 12px !important;
}
.result-card-decode {
    background: rgba(139, 92, 246, 0.08) !important;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
    border-radius: 12px !important;
}

/* Error styling */
.error-text {
    color: #f87171 !important;
    font-weight: 500 !important;
}

/* History items */
.history-item {
    background: #0f172a !important;
    border: 1px solid #1e293b !important;
    border-radius: 12px !important;
    transition: border-color 0.2s ease !important;
}
.history-item:hover {
    border-color: #334155 !important;
}
.history-time {
    color: #475569 !important;
    font-size: 0.75rem !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.history-input {
    color: #cbd5e1 !important;
    font-size: 0.875rem !important;
}
.history-output {
    color: #06b6d4 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.875rem !important;
    letter-spacing: 1px !important;
}

/* Buttons */
.btn-encode {
    background: linear-gradient(135deg, #06b6d4, #0891b2) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    text-transform: none !important;
    padding: 8px 24px !important;
    box-shadow: 0 4px 14px rgba(6, 182, 212, 0.3) !important;
}
.btn-encode:hover {
    box-shadow: 0 6px 20px rgba(6, 182, 212, 0.5) !important;
}
.btn-decode {
    background: linear-gradient(135deg, #8b5cf6, #7c3aed) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    text-transform: none !important;
    padding: 8px 24px !important;
    box-shadow: 0 4px 14px rgba(139, 92, 246, 0.3) !important;
}
.btn-decode:hover {
    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5) !important;
}
.btn-clear {
    color: #64748b !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    text-transform: none !important;
    font-weight: 500 !important;
}
.btn-clear:hover {
    background: rgba(100, 116, 139, 0.1) !important;
}

/* Reference grid */
.ref-card {
    background: #0f172a !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
    padding: 6px 10px !important;
}
.ref-char {
    font-weight: 700 !important;
    color: #8b5cf6 !important;
    font-size: 0.9rem !important;
}
.ref-morse {
    font-family: 'JetBrains Mono', monospace !important;
    color: #06b6d4 !important;
    font-size: 0.8rem !important;
    letter-spacing: 2px !important;
}

/* Custom textarea */
.dark-textarea .q-field__control {
    background: #0f172a !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
}
.dark-textarea .q-field__label {
    color: #64748b !important;
}
.dark-textarea .q-field__native {
    color: #e2e8f0 !important;
}
.dark-textarea .q-field__control:focus-within {
    border-color: #06b6d4 !important;
}

/* Divider */
.custom-divider {
    border-color: #1e293b !important;
    opacity: 1 !important;
}

/* Footer */
.footer-text {
    color: #475569 !important;
    font-size: 0.8rem !important;
}

/* Expansion panels */
.dark-expansion .q-expansion-item__container {
    border: none !important;
}
.dark-expansion .q-item__label {
    color: #f1f5f9 !important;
    font-weight: 600 !important;
}
.dark-expansion .q-icon {
    color: #64748b !important;
}
</style>
"""

# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------


@ui.page("/")
def index():
    ui.add_head_html(CUSTOM_CSS)
    ui.dark_mode(True)

    # -- state ---------------------------------------------------------------
    text_input = {"ref": None}
    morse_input = {"ref": None}
    text_result_area = {"ref": None}
    morse_result_area = {"ref": None}
    history_container = {"ref": None}

    # -- helpers -------------------------------------------------------------
    def refresh_history():
        container = history_container["ref"]
        container.clear()
        entries = load_history()
        if not entries:
            with container:
                ui.label("Noch keine Konvertierungen vorhanden.").style(
                    "color: #475569; font-style: italic;"
                )
            return
        for entry in reversed(entries[-50:]):
            ts = entry.get("timestamp", "")
            try:
                dt = datetime.fromisoformat(ts)
                ts_fmt = dt.strftime("%d.%m.%Y %H:%M:%S")
            except (ValueError, TypeError):
                ts_fmt = ts
            with container:
                with ui.element("div").classes("history-item q-pa-sm q-mb-xs"):
                    with ui.row().classes("items-center gap-2"):
                        ui.icon("schedule", size="14px").style("color: #475569;")
                        ui.label(ts_fmt).classes("history-time")
                    ui.label(entry.get("input", "")).classes("history-input q-mt-xs")
                    ui.label(entry.get("output", "")).classes("history-output q-mt-xs")

    # -- page layout ---------------------------------------------------------
    with ui.column().classes("w-full items-center q-pa-lg main-container"):

        # Hero
        with ui.column().classes("items-center q-mb-lg q-mt-md").style("gap: 4px;"):
            ui.label("Morse Code Converter").classes("hero-title")
            ui.label(
                "Text und Morse-Code einfach konvertieren"
            ).classes("hero-subtitle")

        # ====== TEXT → MORSE ================================================
        with ui.element("div").classes("converter-card w-full q-pa-lg q-mb-md"):
            with ui.row().classes("items-center gap-3 q-mb-md"):
                ui.icon("edit_note", size="28px").style("color: #06b6d4;")
                with ui.column().style("gap: 0;"):
                    ui.label("ENCODER").classes("section-label")
                    ui.label("Text → Morse").classes("section-title")

            text_input["ref"] = ui.textarea(
                label="Text eingeben",
                placeholder="z.B. HALLO WELT",
            ).classes("w-full dark-textarea").props("outlined")

            text_result_area["ref"] = ui.column().classes("w-full")

            def on_encode():
                val = text_input["ref"].value or ""
                result_col = text_result_area["ref"]
                result_col.clear()
                if not val.strip():
                    ui.notification("Bitte Text eingeben!", type="warning")
                    return
                result, err = encode_gui(val)
                with result_col:
                    if err:
                        ui.label(err).classes("error-text q-mt-sm")
                    else:
                        with ui.element("div").classes(
                            "result-card q-pa-md q-mt-sm w-full"
                        ):
                            ui.label("Ergebnis").style(
                                "color: #64748b; font-size: 0.7rem; "
                                "text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600;"
                            )
                            ui.label(result).classes("morse-output").style(
                                "word-break: break-all; margin-top: 4px;"
                            )
                refresh_history()

            def on_clear_text():
                text_input["ref"].value = ""
                text_result_area["ref"].clear()

            with ui.row().classes("q-mt-md gap-3"):
                ui.button("Konvertieren", on_click=on_encode, icon="bolt").classes(
                    "btn-encode"
                ).props("unelevated no-caps")
                ui.button("Löschen", on_click=on_clear_text, icon="backspace").classes(
                    "btn-clear"
                ).props("flat no-caps")

        # ====== MORSE → TEXT ================================================
        with ui.element("div").classes("converter-card w-full q-pa-lg q-mb-md"):
            with ui.row().classes("items-center gap-3 q-mb-md"):
                ui.icon("hearing", size="28px").style("color: #8b5cf6;")
                with ui.column().style("gap: 0;"):
                    ui.label("DECODER").classes("section-label")
                    ui.label("Morse → Text").classes("section-title")

            morse_input["ref"] = ui.textarea(
                label="Morse-Code eingeben",
                placeholder="z.B. .... .- .-.. .-.. --- / .-- . .-.. -",
            ).classes("w-full dark-textarea").props("outlined")
            ui.label(
                "Buchstaben mit Leerzeichen trennen  |  / = Wortabstand"
            ).style("color: #475569; font-size: 0.75rem; margin-top: 4px;")

            morse_result_area["ref"] = ui.column().classes("w-full")

            def on_decode():
                val = morse_input["ref"].value or ""
                result_col = morse_result_area["ref"]
                result_col.clear()
                if not val.strip():
                    ui.notification("Bitte Morse-Code eingeben!", type="warning")
                    return
                result, err = decode_gui(val)
                with result_col:
                    if err:
                        ui.label(err).classes("error-text q-mt-sm")
                    else:
                        with ui.element("div").classes(
                            "result-card-decode q-pa-md q-mt-sm w-full"
                        ):
                            ui.label("Ergebnis").style(
                                "color: #64748b; font-size: 0.7rem; "
                                "text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600;"
                            )
                            ui.label(result).style(
                                "color: #c4b5fd; font-size: 1.25rem; "
                                "font-weight: 700; margin-top: 4px; letter-spacing: 2px;"
                            )
                refresh_history()

            def on_clear_morse():
                morse_input["ref"].value = ""
                morse_result_area["ref"].clear()

            with ui.row().classes("q-mt-md gap-3"):
                ui.button("Dekodieren", on_click=on_decode, icon="translate").classes(
                    "btn-decode"
                ).props("unelevated no-caps")
                ui.button(
                    "Löschen", on_click=on_clear_morse, icon="backspace"
                ).classes("btn-clear").props("flat no-caps")

        # ====== ZEICHENREFERENZ =============================================
        with ui.element("div").classes("converter-card w-full q-pa-lg q-mb-md"):
            with ui.row().classes("items-center gap-3 q-mb-md"):
                ui.icon("grid_on", size="28px").style("color: #ec4899;")
                with ui.column().style("gap: 0;"):
                    ui.label("REFERENZ").classes("section-label")
                    ui.label("Unterstützte Zeichen").classes("section-title")

            with ui.expansion("Zeichentabelle anzeigen", icon="visibility").classes(
                "w-full dark-expansion"
            ):
                with ui.grid(columns=4).classes("w-full").style("gap: 8px;"):
                    for char, morse in TO_MORSE_DICT.items():
                        display_char = "SPACE" if char == " " else char
                        with ui.element("div").classes("ref-card"):
                            with ui.row().classes("items-center justify-between"):
                                ui.label(display_char).classes("ref-char")
                                ui.label(morse).classes("ref-morse")

        # ====== VERLAUF =====================================================
        with ui.element("div").classes("converter-card w-full q-pa-lg q-mb-md"):
            with ui.row().classes("items-center gap-3 q-mb-md"):
                ui.icon("history", size="28px").style("color: #f59e0b;")
                with ui.column().style("gap: 0;"):
                    ui.label("HISTORY").classes("section-label")
                    ui.label("Verlauf").classes("section-title")

            def on_clear_history():
                clear_history_file()
                refresh_history()
                ui.notification("Verlauf gelöscht!", type="info")

            def on_download_history():
                entries = load_history()
                if not entries:
                    ui.notification("Kein Verlauf vorhanden!", type="warning")
                    return
                content = json.dumps(entries, indent=4, ensure_ascii=False)
                filename = (
                    f"morse_history_{datetime.now().strftime('%Y-%m-%d')}.json"
                )
                ui.download(content.encode("utf-8"), filename)

            with ui.row().classes("gap-3 q-mb-md"):
                ui.button(
                    "Löschen", on_click=on_clear_history, icon="delete_sweep"
                ).classes("btn-clear").props("flat no-caps").style(
                    "color: #f87171 !important; border-color: #7f1d1d !important;"
                )
                ui.button(
                    "Herunterladen",
                    on_click=on_download_history,
                    icon="download",
                ).classes("btn-clear").props("flat no-caps").style(
                    "color: #06b6d4 !important; border-color: #164e63 !important;"
                )

            history_container["ref"] = ui.column().classes("w-full").style(
                "max-height: 400px; overflow-y: auto; gap: 8px;"
            )
            refresh_history()

        # Footer
        ui.label("Morse Code Converter — GrPro Projekt").classes(
            "footer-text q-mt-lg q-mb-md"
        )


ui.run(title="Morse Code Converter", port=8080, reload=False)
