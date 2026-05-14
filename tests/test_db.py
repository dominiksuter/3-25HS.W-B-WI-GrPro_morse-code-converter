from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest
from sqlalchemy import inspect, select
from sqlalchemy.exc import IntegrityError


APP_DIR = Path(__file__).resolve().parents[1] / "app"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


@pytest.fixture
def fresh_db(tmp_path, monkeypatch):
    db_file = tmp_path / "morse_chat_test.db"
    monkeypatch.setenv("DBPATH", str(db_file))

    import db.database_manager as database_manager

    importlib.reload(database_manager)

    from db.database_manager import DatabaseManager

    DatabaseManager.init_db()
    return DatabaseManager


def test_init_db_creates_expected_tables(fresh_db) -> None:
    from db.database_manager import DatabaseManager

    inspector = inspect(DatabaseManager.engine)
    tables = set(inspector.get_table_names())

    assert {"users", "chats", "messages"}.issubset(tables)


def test_user_auid_is_unique(fresh_db) -> None:
    from db.database_manager import DatabaseManager
    from db.models.user import User

    with DatabaseManager.session() as session:
        session.add(User(id="same-id"))
        session.commit()

        session.add(User(id="same-id"))
        with pytest.raises(IntegrityError):
            session.commit()


def test_delete_chat_deletes_related_messages(fresh_db) -> None:
    from db.database_manager import DatabaseManager
    from db.models.chat import Chat
    from db.models.message import Message
    from db.models.user import User

    with DatabaseManager.session() as session:
        user = User(id="test-id")
        chat = Chat(title="Test")
        chat.user = user
        chat.messages.append(Message(content="HI", is_morse=False))

        session.add(chat)
        session.commit()

        session.delete(chat)
        session.commit()

        remaining = session.execute(select(Message)).scalars().all()
        assert remaining == []
