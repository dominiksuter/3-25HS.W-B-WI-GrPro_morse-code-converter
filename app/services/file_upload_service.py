"""File upload handling and validation service."""

import re

from services.morse_converter import ConversionError, MorseConverter


class FileUploadError(Exception):
    """Base exception for file upload errors."""

    pass


class InvalidFileFormatError(FileUploadError):
    """Raised when file format is not .txt."""

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
    def process_upload(filename: str, content_type: str, raw_text: str) -> str:
        """
        Validate filename/content-type and normalize the raw text.

        The caller is responsible for reading the file (NiceGUI's FileUpload
        API is async-only); this service stays sync.

        Args:
            filename: Original filename from the upload.
            content_type: MIME type from the upload.
            raw_text: Already-decoded UTF-8 file content.

        Returns:
            Normalized content string (whitespace-collapsed).

        Raises:
            InvalidFileFormatError: If file is not .txt.
            EmptyFileError: If file is empty after normalization.

        """
        FileUploadService._validate_file_format(filename, content_type)
        content = " ".join((raw_text or "").split()).strip()
        FileUploadService._validate_empty(content)
        return content

    @staticmethod
    def _validate_file_format(filename: str, content_type: str) -> None:
        """Validate that uploaded file is a .txt file."""
        name = (filename or "").strip()
        mime = (content_type or "").strip().lower()

        is_txt_by_name = bool(name) and name.lower().endswith(".txt")
        is_txt_by_mime = mime.startswith("text/") or mime == ""

        if not is_txt_by_name and not (not name and is_txt_by_mime):
            raise InvalidFileFormatError(
                "Dateiformat nicht erlaubt. Nur .txt-Dateien möglich."
            )

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
