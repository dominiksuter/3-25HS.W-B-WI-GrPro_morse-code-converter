from pathlib import Path

from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DB_PATH = Path(__file__).resolve().parent.parent / "morse_chat.db"

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class Base(DeclarativeBase):
    pass


def init_db() -> None:
    from app.models.chat import Chat  # noqa: F401
    from app.models.message import Message  # noqa: F401

    Base.metadata.create_all(engine)

    # lightweight SQLite migration (no Alembic): add missing columns as needed
    with engine.begin() as conn:
        cols = [row[1] for row in conn.execute(text('PRAGMA table_info("chats")')).fetchall()]
        if "unpinned_updated_at" not in cols:
            conn.execute(text('ALTER TABLE "chats" ADD COLUMN "unpinned_updated_at" DATETIME'))
            conn.execute(
                text(
                    'UPDATE "chats" SET "unpinned_updated_at" = "updated_at" '
                    'WHERE "unpinned_updated_at" IS NULL'
                )
            )
