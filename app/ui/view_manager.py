"""UI application management and startup."""

from pathlib import Path

from nicegui import ui

from .app_layout import register_pages
from .styles import CUSTOM_CSS


class ViewManager:
    """Coordinates UI initialization and NiceGUI app startup."""

    def __init__(
        self,
        *,
        title: str = "Morse-Code Konverter",
        host: str = "localhost",
        port: int = 8080,
        reload: bool = False,
        storage_secret: str,
        favicon_path: str = "./favicon.png",
        show: bool = True,
    ) -> None:
        self.title = title
        self.host = host
        self.port = port
        self.reload = reload
        self.storage_secret = storage_secret
        self.favicon_path = favicon_path
        self.show = show

    def setup_styles(self) -> None:
        """Register global CSS styles (app-wide, once at startup)."""
        ui.add_head_html(CUSTOM_CSS, shared=True)

    def setup_pages(self) -> None:
        """Register all page routes."""
        register_pages()

    def run(self) -> None:
        """Initialize and start the NiceGUI application."""
        self.setup_styles()
        self.setup_pages()
        ui.run(
            title=self.title,
            host=self.host,
            port=self.port,
            reload=self.reload,
            storage_secret=self.storage_secret,
            favicon=str(Path(self.favicon_path)),
            show=self.show,
        )