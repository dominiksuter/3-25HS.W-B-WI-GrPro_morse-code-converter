from __future__ import annotations

import sys
from pathlib import Path

import pytest

APP_DIR = Path(__file__).resolve().parents[1] / "app"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


def test_encode_text_to_morse_sos() -> None:
    from services.morse_converter import MorseConverter

    assert MorseConverter.encode("SOS") == "... --- ..."


def test_decode_morse_to_text_sos() -> None:
    from services.morse_converter import MorseConverter

    assert MorseConverter.decode("... --- ...") == "SOS"


def test_encode_unsupported_character_raises() -> None:
    from services.morse_converter import ConversionError, MorseConverter

    with pytest.raises(ConversionError):
        MorseConverter.encode("Hello 😊")
