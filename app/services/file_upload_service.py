"""File upload handling and validation service."""

import re
from typing import Any

from services.morse_converter import ConversionError, MorseConverter


class FileUploadError(Exception):
    """Base exception for file upload errors."""

    pass


class InvalidFileFormatError(FileUploadError):
    """Raised when file format is not .txt."""

    pass


class FileEncodingError(FileUploadError):
    """Raised when file is not valid UTF-8."""

    pass


class FileReadError(FileUploadError):
    """Raised when file cannot be read."""

    pass


class EmptyFileError(FileUploadError):
    """Raised when file is empty."""

    pass


class MixedContentError(FileUploadError):
    """Raised when file contains mixed text and Morse code."""

    pass


class InvalidCharactersError(FileUploadError):
    """Raised when file contains invalid characters."""

    pass


class InvalidMorseError(FileUploadError):
    """Raised when Morse code content is invalid."""

    pass


class FileUploadService:
    """Service for handling file uploads with validation."""

    MAX_FILE_SIZE_KILOBYTES = 5
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_KILOBYTES * 1024

    @staticmethod
    async def process_upload(upload: Any) -> str:
        """
        Process an uploaded file and return its normalized content.

        Args:
            upload: The uploaded file object from NiceGUI.

        Returns:
            Normalized content string.

        Raises:
            InvalidFileFormatError: If file is not .txt.
            FileEncodingError: If file is not UTF-8.
            FileReadError: If file cannot be read.
            EmptyFileError: If file is empty.
            MixedContentError: If file contains mixed text and Morse.
            InvalidCharactersError: If text contains unsupported characters.
            InvalidMorseError: If Morse code is invalid.

        """
        FileUploadService._validate_file_format(upload)
        content = await FileUploadService._read_file_content(upload)
        FileUploadService._validate_empty(content)

        return content

    @staticmethod
    def _validate_file_format(upload: Any) -> None:
        """Validate that uploaded file is a .txt file."""
        filename = (getattr(upload, "name", "") or "").strip()
        content_type = (
            (getattr(upload, "content_type", "") or "").strip().lower()
        )

        is_txt_by_name = bool(filename) and filename.lower().endswith(".txt")
        is_txt_by_mime = content_type.startswith("text/") or content_type == ""

        if not is_txt_by_name and not (not filename and is_txt_by_mime):
            raise InvalidFileFormatError(
                "Dateiformat nicht erlaubt. Nur .txt-Dateien möglich."
            )

    @staticmethod
    async def _read_file_content(upload: Any) -> str:
        """Read file content with UTF-8 encoding."""
        try:
            raw = await upload.text(encoding="utf-8")
        except UnicodeDecodeError:
            raise FileEncodingError("Datei ist keine gültige UTF-8 Textdatei.")
        except Exception:
            raise FileReadError("Datei konnte nicht gelesen werden.")

        # Normalize whitespace (allow multi-line files)
        content = " ".join((raw or "").split()).strip()
        return content

    @staticmethod
    def _validate_empty(content: str) -> None:
        """Validate that content is not empty."""
        if not content:
            raise EmptyFileError("Datei ist leer.")

    @staticmethod
    def validate_content(content: str) -> str:
        """
        Validate content for mixed Morse/text and invalid characters.

        Args:
            content: Normalized content string.

        Returns:
            The validated content.

        Raises:
            MixedContentError: If content mixes text and Morse.
            InvalidCharactersError: If text contains unsupported characters.
            InvalidMorseError: If Morse code is invalid.

        """
        # Decide whether content is Morse-only or Text-only
        is_morse_only = MorseConverter.is_morse(content)

        if is_morse_only:
            # Validate Morse tokens
            try:
                MorseConverter.decode(content)
            except ConversionError as exc:
                raise InvalidMorseError(str(exc))
            return content

        # Reject mixed files: letters + standalone morse tokens
        has_letter = any(ch.isalpha() for ch in content)
        has_morse_token = (
            re.search(r"(^|\s)[.-]{1,6}(?=\s|/|$)", content) is not None
        )
        if has_letter and has_morse_token:
            msg = (
                "Datei enthält gemischten Inhalt (Text und Morse-Code). "
                "Bitte nur eines davon."
            )
            raise MixedContentError(msg)

        # Validate allowed characters for text
        invalid = sorted(
            {ch for ch in content.upper() if ch not in MorseConverter.TO_MORSE}
        )
        if invalid:
            preview = ", ".join(invalid[:8])
            more = " …" if len(invalid) > 8 else ""
            raise InvalidCharactersError(
                f"Ungültige Zeichen in Datei: {preview}{more}"
            )

        return content
