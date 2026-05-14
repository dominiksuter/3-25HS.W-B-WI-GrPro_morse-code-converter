"""User management for session-backed anonymous users."""

from nicegui import app as nicegui_app


class UserManager:
    """Handles anonymous user id (auid) persistence."""

    SESSION_AUID_KEY = "auid"

    @staticmethod
    def anonymous_session_user() -> str:
        """Return the session's anonymous user id, creating one if missing."""
        if UserManager.SESSION_AUID_KEY not in nicegui_app.storage.user:
            import uuid

            nicegui_app.storage.user[UserManager.SESSION_AUID_KEY] = str(
                uuid.uuid4()
            )
        return str(nicegui_app.storage.user[UserManager.SESSION_AUID_KEY])
