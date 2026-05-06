from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.chat import Chat


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("chats.id", ondelete="CASCADE")
    )
    content: Mapped[str] = mapped_column(String, default="")
    is_morse: Mapped[bool] = mapped_column(Boolean, default=False)
    is_error: Mapped[bool] = mapped_column(Boolean, default=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")  # noqa: F821

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "content": self.content,
            "is_morse": self.is_morse,
            "is_error": self.is_error,
            "timestamp": self.timestamp.isoformat(timespec="seconds"),
        }
