from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.message import Message


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(120), default="Neuer Chat")
    pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    # Sort key for the unpinned chat history. This is intentionally NOT updated while a chat is pinned
    # so that removing the pin restores the chat to its previous position.
    unpinned_updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="chat",
        cascade="all, delete-orphan",
        order_by="Message.timestamp",
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
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
