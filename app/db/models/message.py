import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .chat import Chat


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    chat_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("chats.id", ondelete="CASCADE")
    )
    content: Mapped[str] = mapped_column(String, default="")
    is_morse: Mapped[bool] = mapped_column(Boolean, default=False)
    is_error: Mapped[bool] = mapped_column(Boolean, default=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")  # noqa: F821

    def to_dict(self) -> dict:
        """Convert message to dictionary representation.

        Returns:
            Dictionary with message data.

        """
        return {
            "id": self.id,
            "content": self.content,
            "is_morse": self.is_morse,
            "is_error": self.is_error,
            "timestamp": self.timestamp.isoformat(timespec="seconds"),
        }
