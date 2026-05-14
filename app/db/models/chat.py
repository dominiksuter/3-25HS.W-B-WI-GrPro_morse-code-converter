from datetime import datetime
from typing import TYPE_CHECKING
import uuid

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .message import Message
    from .user import User


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(120), default="Neuer Chat")
    pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )
    # Sort key for the unpinned chat history. This is intentionally NOT updated while a chat is pinned
    # so that removing the pin restores the chat to its previous position.
    unpinned_updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="chat",
        cascade="all, delete-orphan",
        order_by="Message.timestamp",
    )
    user: Mapped["User"] = relationship("User", back_populates="chats")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "pinned": self.pinned,
            "created_at": self.created_at.isoformat(timespec="seconds"),
            "unpinned_updated_at": (
                self.unpinned_updated_at.isoformat(timespec="seconds")
                if self.unpinned_updated_at is not None
                else None
            ),
            "updated_at": self.updated_at.isoformat(timespec="seconds"),
            "messages": [m.to_dict() for m in self.messages],
        }
