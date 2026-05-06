import os

from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from db.models.base import Base


db_env = os.getenv("DBPATH", "./morse_chat.db")
DB_PATH = Path(db_env)

# Ensure the database directory exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


class DatabaseManager:
    engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
    SessionLocal = sessionmaker(
        bind=engine, autoflush=False, autocommit=False, future=True
    )

    @classmethod
    def session(cls):
        return cls.SessionLocal()

    @classmethod
    def init_db(cls) -> None:
        from db.models.chat import Chat  # noqa: F401
        from db.models.message import Message  # noqa: F401

        Base.metadata.create_all(cls.engine)

        # lightweight SQLite migration (no Alembic): add missing columns as needed
        with cls.engine.begin() as conn:
            cols = [
                row[1]
                for row in conn.execute(
                    text('PRAGMA table_info("chats")')
                ).fetchall()
            ]
            if "unpinned_updated_at" not in cols:
                conn.execute(
                    text(
                        'ALTER TABLE "chats" ADD COLUMN "unpinned_updated_at" DATETIME'
                    )
                )
                conn.execute(
                    text(
                        'UPDATE "chats" SET "unpinned_updated_at" = "updated_at" '
                        'WHERE "unpinned_updated_at" IS NULL'
                    )
                )
