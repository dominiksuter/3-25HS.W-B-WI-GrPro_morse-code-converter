import os

from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from .models.base import Base


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
        from db.models.user import User  # noqa: F401

        Base.metadata.create_all(cls.engine)
