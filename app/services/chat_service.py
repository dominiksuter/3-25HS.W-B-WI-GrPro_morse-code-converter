import json
from datetime import datetime

from sqlalchemy import case, select
from sqlalchemy.orm import Session, joinedload

from db.database_manager import DatabaseManager
from db.models.chat import Chat
from db.models.message import Message
from services.morse_converter import ConversionError, MorseConverter


class ChatService:
    """Application logic for managing chats and messages.

    Each public method opens its own session so the UI layer doesn't have
    to deal with persistence concerns.
    """

    @staticmethod
    def _session() -> Session:
        return DatabaseManager.session()

    def list_chats(self) -> list[Chat]:
        with self._session() as session:
            sort_key = case(
                (Chat.pinned.is_(True), Chat.updated_at),
                else_=Chat.unpinned_updated_at,
            )
            stmt = (
                select(Chat)
                .options(joinedload(Chat.messages))
                .order_by(
                    Chat.pinned.desc(), sort_key.desc(), Chat.created_at.desc()
                )
            )
            chats = session.execute(stmt).unique().scalars().all()
            session.expunge_all()
            return list(chats)

    def get_chat(self, chat_id: int) -> Chat | None:
        with self._session() as session:
            stmt = (
                select(Chat)
                .options(joinedload(Chat.messages))
                .where(Chat.id == chat_id)
            )
            chat = session.execute(stmt).unique().scalar_one_or_none()
            if chat is not None:
                session.expunge(chat)
            return chat

    def create_chat(self, title: str = "Neuer Chat") -> Chat:
        with self._session() as session:
            now = datetime.now()
            chat = Chat(
                title=title,
                created_at=now,
                updated_at=now,
                unpinned_updated_at=now,
            )
            session.add(chat)
            session.commit()
            session.refresh(chat)
            session.expunge(chat)
            return chat

    def delete_chat(self, chat_id: int) -> None:
        with self._session() as session:
            chat = session.get(Chat, chat_id)
            if chat is not None:
                session.delete(chat)
                session.commit()

    def toggle_pin(self, chat_id: int) -> bool:
        with self._session() as session:
            chat = session.get(Chat, chat_id)
            if chat is None:
                return False
            if chat.unpinned_updated_at is None:
                chat.unpinned_updated_at = chat.updated_at
            chat.pinned = not chat.pinned
            session.commit()
            return chat.pinned

    def rename_chat(self, chat_id: int, title: str) -> None:
        with self._session() as session:
            chat = session.get(Chat, chat_id)
            if chat is not None:
                chat.title = title or "Neuer Chat"
                session.commit()

    def clear_messages(self, chat_id: int) -> None:
        with self._session() as session:
            chat = session.get(Chat, chat_id)
            if chat is None:
                return
            for message in list(chat.messages):
                session.delete(message)
            session.commit()

    def delete_message(self, message_id: int) -> None:
        with self._session() as session:
            msg = session.get(Message, message_id)
            if msg is not None:
                session.delete(msg)
                session.commit()

    def send_message(self, chat_id: int, raw_input: str) -> list[Message]:
        """Persist the user's input + the converted response (or an error)."""
        cleaned = raw_input.strip()
        if not cleaned:
            raise ConversionError("Bitte etwas eingeben.")

        input_is_morse = MorseConverter.is_morse(cleaned)
        try:
            output, output_is_morse = MorseConverter.convert(cleaned)
            error = False
        except ConversionError as exc:
            output = str(exc)
            output_is_morse = False
            error = True

        with self._session() as session:
            chat = session.get(Chat, chat_id)
            if chat is None:
                raise ValueError(f"Chat {chat_id} not found")

            user_msg = Message(
                chat_id=chat_id,
                content=cleaned,
                is_morse=input_is_morse,
            )
            bot_msg = Message(
                chat_id=chat_id,
                content=output,
                is_morse=output_is_morse and not error,
                is_error=error,
            )
            session.add_all([user_msg, bot_msg])

            if not chat.messages and not error:
                chat.title = (
                    (cleaned[:30] + "…") if len(cleaned) > 30 else cleaned
                )
            now = datetime.now()
            chat.updated_at = now
            # Keep the unpinned history position stable while pinned.
            if not chat.pinned:
                chat.unpinned_updated_at = now

            session.commit()
            session.refresh(user_msg)
            session.refresh(bot_msg)
            session.expunge_all()
            return [user_msg, bot_msg]

    def export_chat_json(self, chat_id: int) -> str | None:
        chat = self.get_chat(chat_id)
        if chat is None:
            return None
        return json.dumps(chat.to_dict(), indent=2, ensure_ascii=False)

    def import_text_file(self, chat_id: int, content: str) -> list[Message]:
        return self.send_message(chat_id, content)
