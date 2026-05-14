from __future__ import annotations

import sys
from pathlib import Path

import pytest

APP_DIR = Path(__file__).resolve().parents[1] / "app"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


def test_encode_text_to_morse_sos() -> None:
    """TC_001: Encode text to Morse (SOS).

    Verifies that encoding the string "SOS" produces the expected
    Morse code sequence.
    """
    from services.morse_converter import MorseConverter

    assert MorseConverter.encode("SOS") == "... --- ..."


def test_decode_morse_to_text_sos() -> None:
    """TC_002: Decode Morse to text (SOS).

    Verifies that decoding the Morse sequence "... --- ..." returns
    the text "SOS".
    """
    from services.morse_converter import MorseConverter

    assert MorseConverter.decode("... --- ...") == "SOS"


def test_encode_unsupported_character_raises() -> None:
    """TC_003: Reject unsupported text characters.

    Ensures that attempting to encode unsupported characters (emoji)
    raises a ConversionError.
    """
    from services.morse_converter import ConversionError, MorseConverter

    with pytest.raises(ConversionError):
        MorseConverter.encode("Hello 😊")
