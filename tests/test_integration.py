from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest


APP_DIR = Path(__file__).resolve().parents[1] / "app"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


@pytest.fixture
def fresh_db(tmp_path, monkeypatch):
    """Create a fresh SQLite DB and reload the DB/service modules.

    `db.database_manager` reads DBPATH at import time, so we reload it.
    """

    db_file = tmp_path / "morse_chat_test.db"
    monkeypatch.setenv("DBPATH", str(db_file))

    import db.database_manager as database_manager

    importlib.reload(database_manager)

    from db.database_manager import DatabaseManager

    DatabaseManager.init_db()

    import services.chat_service as chat_service

    importlib.reload(chat_service)

    return DatabaseManager


def test_create_chat_and_list_chats(fresh_db) -> None:
    from services.chat_service import ChatService

    service = ChatService(user_auid="test-auid")
    c1 = service.create_chat(title="Chat 1")
    c2 = service.create_chat(title="Chat 2")

    chats = service.list_chats()
    ids = {c.id for c in chats}
    assert c1.id in ids
    assert c2.id in ids


def test_send_message_creates_user_and_two_messages(fresh_db) -> None:
    from services.chat_service import ChatService

    service = ChatService(user_auid="test-auid")
    chat = service.create_chat()

    messages = service.send_message(chat.id, "HI")
    assert len(messages) == 2

    user_msg, bot_msg = messages
    assert user_msg.content == "HI"
    assert user_msg.is_morse is False

    assert bot_msg.content == ".... .."
    assert bot_msg.is_morse is True
    assert bot_msg.is_error is False


def test_export_chat_json_contains_messages(fresh_db) -> None:
    from services.chat_service import ChatService

    service = ChatService(user_auid="test-auid")
    chat = service.create_chat()
    service.send_message(chat.id, "SOS")

    payload = service.export_chat_json(chat.id)
    assert payload is not None

    data = json.loads(payload)
    assert data["id"] == chat.id
    assert len(data["messages"]) == 2


def test_toggle_pin_toggles_state(fresh_db) -> None:
    from services.chat_service import ChatService

    service = ChatService(user_auid="test-auid")
    chat = service.create_chat()

    assert service.toggle_pin(chat.id) is True
    assert service.toggle_pin(chat.id) is False
