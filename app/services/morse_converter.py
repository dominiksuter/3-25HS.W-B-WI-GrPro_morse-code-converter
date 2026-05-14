class ConversionError(Exception):
    pass


class MorseConverter:
    TO_MORSE: dict[str, str] = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
        "0": "-----",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        ".": ".-.-.-",
        ",": "--..--",
        "?": "..--..",
        "/": "-..-.",
        "-": "-....-",
        "(": "-.--.",
        ")": "-.--.-",
        " ": "/",
    }

    TO_TEXT: dict[str, str] = {v: k for k, v in TO_MORSE.items()}

    MORSE_CHARS: set[str] = set(".-/ ")

    @classmethod
    def is_morse(cls, value: str) -> bool:
        """Check if a string contains only Morse code characters."""
        stripped = value.strip()
        if not stripped:
            return False
        return all(ch in cls.MORSE_CHARS for ch in stripped)

    @classmethod
    def encode(cls, text: str) -> str:
        """Convert text to Morse code."""
        if not text.strip():
            raise ConversionError("Bitte Text eingeben.")
        encoded: list[str] = []
        for ch in text.upper():
            if ch not in cls.TO_MORSE:
                raise ConversionError(
                    f"'{ch}' kann nicht in Morse-Code dargestellt werden."
                )
            encoded.append(cls.TO_MORSE[ch])
        return " ".join(encoded)

    @classmethod
    def decode(cls, morse: str) -> str:
        """Convert Morse code to text."""
        if not morse.strip():
            raise ConversionError("Bitte Morse-Code eingeben.")
        decoded: list[str] = []
        for code in morse.strip().split(" "):
            if code == "":
                continue
            if code not in cls.TO_TEXT:
                raise ConversionError(
                    f"'{code}' ist kein gültiger Morse-Buchstabe."
                )
            decoded.append(cls.TO_TEXT[code])
        return "".join(decoded)

    @classmethod
    def convert(cls, value: str) -> tuple[str, bool]:
        """Auto-detect direction. Returns (result, result_is_morse)."""
        if cls.is_morse(value):
            return cls.decode(value), False
        return cls.encode(value), True

    @classmethod
    def reference_table(cls) -> list[tuple[str, str]]:
        """Return all supported character to Morse code mappings."""
        return [
            ("SPACE" if ch == " " else ch, code)
            for ch, code in cls.TO_MORSE.items()
        ]
