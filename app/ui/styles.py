CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Material+Icons+Outlined&display=swap');

html, body {
    margin: 0;
    height: 100%;
    font-family: 'Inter', sans-serif;
    background: #f9fafb;
}
.nicegui-content {
    padding: 0 !important;
    margin: 0 !important;
    width: 100% !important;
    max-width: none !important;
    height: 100vh !important;
}

/* App shell */
.app-shell { display: flex; height: 100vh; width: 100%; background: #f9fafb; }

/* Sidebar */
.sidebar {
    width: 256px;
    background: #111827;
    color: #ffffff;
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
}
.sidebar-header { padding: 16px; border-bottom: 1px solid #374151; }
.sidebar-new-btn {
    width: 100% !important;
    background: #1f2937 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    font-weight: 500 !important;
    text-transform: none !important;
}
.sidebar-new-btn:hover { background: #374151 !important; }
.sidebar-list { flex: 1; overflow-y: auto; padding: 8px; }
.sidebar-empty {
    color: #6b7280;
    font-size: 0.875rem;
    text-align: center;
    padding: 16px;
}
.chat-row {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 12px;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.15s;
    color: #e5e7eb;
}
.chat-row:hover { background: #1f2937; }
.chat-row.active { background: #1f2937; }
.chat-row .title { flex: 1; font-size: 0.875rem; overflow: hidden;
    text-overflow: ellipsis; white-space: nowrap; }
.chat-row .actions { opacity: 0; transition: opacity 0.15s; display: flex; gap: 2px; }
.chat-row:hover .actions { opacity: 1; }
.chat-row.active .actions { opacity: 1; }
.icon-btn {
    background: transparent !important;
    color: #9ca3af !important;
    padding: 4px !important;
    min-width: 0 !important;
    border-radius: 4px !important;
}
.icon-btn:hover { background: #374151 !important; color: #ffffff !important; }
/* Pin button should behave like other row actions: visible on hover (or if pinned/active) */
.pin-btn { opacity: 0; transition: opacity 0.15s; }
.chat-row:hover .pin-btn,
.chat-row.active .pin-btn,
.pin-btn.pinned { opacity: 1; }
.pin-btn.pinned { color: #f3f4f6 !important; }
.sidebar-footer {
    padding: 16px;
    border-top: 1px solid #374151;
    color: #6b7280;
    font-size: 0.75rem;
}

/* Main content */
.main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: #ffffff;
    min-width: 0;
}
.chat-header {
    border-bottom: 1px solid #e5e7eb;
    padding: 16px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #ffffff;
}
.chat-header h1 { font-size: 1.25rem; font-weight: 600; color: #111827; margin: 0; line-height: 1.2; }
.chat-header p { font-size: 0.875rem; color: #6b7280; margin: 0; }

.messages-area {
    flex: 1;
    overflow-y: auto;
    padding: 16px 24px;
    background: #ffffff;
}
.messages-inner { max-width: 768px; margin: 0 auto; display: flex;
    flex-direction: column; gap: 12px; }

/* Welcome screen */
.welcome-wrap {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.welcome-card { text-align: center; max-width: 480px; }
.welcome-sos {
    font-family: 'JetBrains Mono', monospace;
    font-size: 3rem;
    color: #111827;
    margin-bottom: 16px;
    letter-spacing: 4px;
}
.welcome-title { font-size: 1.5rem; font-weight: 600; color: #111827; margin: 0 0 8px; }
.welcome-text { color: #4b5563; margin-bottom: 16px; }
.welcome-hint { color: #6b7280; font-size: 0.875rem; }
.welcome-hint p { margin: 4px 0; }

/* Message bubbles */
.bubble-row { display: flex; }
.bubble-row.left { justify-content: flex-start; }
.bubble-row.right { justify-content: flex-end; }
.bubble {
    max-width: 70%;
    padding: 12px 16px;
    border-radius: 12px;
    position: relative;
}
.bubble-morse { background: #f3f4f6; color: #111827; }
.bubble-text { background: #1f2937; color: #ffffff; }
.bubble-error { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
.bubble-label { font-size: 0.75rem; opacity: 0.7; margin-bottom: 4px;
    text-transform: uppercase; letter-spacing: 0.05em; }
.bubble-content { font-family: 'JetBrains Mono', monospace; word-break: break-word; }
.bubble-content.morse { font-size: 1.05rem; letter-spacing: 2px; }

/* Input bar */
.input-bar {
    border-top: 1px solid #e5e7eb;
    padding: 16px 24px;
    background: #ffffff;
}
.input-inner { max-width: 768px; margin: 0 auto; display: flex; gap: 8px; align-items: flex-end; }

/* Attach (file upload) — collapse q-uploader to a round blue icon button */
.attach-btn {
    width: 40px !important;
    min-width: 40px !important;
    max-width: 40px !important;
    height: 40px !important;
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
    overflow: visible !important;
    flex-shrink: 0;
    align-self: center;
}
.attach-btn .q-uploader__header {
    background: transparent !important;
    padding: 0 !important;
    min-height: 0 !important;
    border: none !important;
}
.attach-btn .q-uploader__header::before { display: none !important; }
.attach-btn .q-uploader__header-content {
    padding: 0 !important;
    min-height: 0 !important;
    flex-direction: row !important;
    align-items: center !important;
    flex-wrap: nowrap !important;
}
/* Hide everything except the first add-file button */
.attach-btn .q-uploader__title,
.attach-btn .q-uploader__subtitle,
.attach-btn .q-uploader__list,
.attach-btn .q-uploader__dnd { display: none !important; }
.attach-btn .q-uploader__header-content .q-btn ~ .q-btn { display: none !important; }
/* Restyle the first (add-file) button as a round blue icon button */
.attach-btn .q-uploader__header-content .q-btn:first-of-type {
    width: 40px !important;
    height: 40px !important;
    min-width: 40px !important;
    min-height: 40px !important;
    border-radius: 50% !important;
    background: #1f2937 !important;
    color: #ffffff !important;
    margin: 0 !important;
    padding: 0 !important;
    box-shadow: 0 2px 4px rgba(31,41,55,0.3) !important;
}
.attach-btn .q-uploader__header-content .q-btn:first-of-type:hover {
    background: #374151 !important;
}
.attach-btn .q-uploader__header-content .q-btn:first-of-type .q-icon {
    font-size: 0 !important; /* hide original (usually 'add') ligature */
    color: #ffffff !important;
}
.attach-btn .q-uploader__header-content .q-btn:first-of-type .q-icon::before {
    content: 'attach_file';
    font-size: 20px;
    line-height: 1;
    display: inline-block;
    color: #ffffff;
}
.chat-input { padding: 0 !important; }
.chat-input .q-field__control {
    border: 1px solid #d1d5db !important;
    border-radius: 8px !important;
    padding: 0 12px !important;
    background: #ffffff !important;
    min-height: 48px !important;
}
.chat-input .q-field__control::before,
.chat-input .q-field__control::after { display: none !important; }
.chat-input .q-field__control-container { padding: 0 !important; min-height: 100% !important; }
.chat-input .q-field__native { padding: 0 !important; min-height: 0 !important; }
.chat-input .q-field__control:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 2px rgba(37,99,235,0.2);
}
.send-btn {
    background: #2563eb !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    text-transform: none !important;
    padding: 12px 20px !important;
    font-weight: 500 !important;
    height: 48px;
}
.send-btn:hover { background: #1d4ed8 !important; }
.send-btn[disabled] { background: #d1d5db !important; color: #9ca3af !important; }

.toolbar-btn {
    background: transparent !important;
    color: #4b5563 !important;
    border-radius: 8px !important;
    text-transform: none !important;
    padding: 8px 12px !important;
    font-size: 0.875rem !important;
}
.toolbar-btn:hover { background: #f3f4f6 !important; }

/* Reference dialog */
.ref-dialog {
    width: 96vw;
    height: 92vh;
    max-width: 96vw;
    display: flex;
    flex-direction: column;
    gap: 12px;
}
.ref-actions { margin-top: auto; }
.ref-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 8px;
}
.ref-grid--dense {
    grid-template-columns: repeat(6, minmax(0, 1fr));
    gap: 6px;
}
.ref-cell {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 8px 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    min-width: 0;
}
.ref-grid--dense .ref-cell {
    padding: 6px 10px;
    border-radius: 6px;
}
.ref-char { font-weight: 700; color: #2563eb; }
.ref-morse { font-family: 'JetBrains Mono', monospace; color: #4b5563;
    letter-spacing: 2px; font-size: 0.875rem; }
.ref-grid--dense .ref-morse { letter-spacing: 1.5px; font-size: 0.75rem; }

/* Notifications (ui.notify) */
.q-notification {
    font-size: 1.05rem;
    line-height: 1.3;
}
.q-notification__message {
    padding: 10px 12px;
}
.q-notification__caption {
    font-size: 0.95rem;
}

</style>
"""
