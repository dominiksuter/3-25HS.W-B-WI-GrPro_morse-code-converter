import json
from pathlib import Path
from datetime import datetime

# Datenbank mit Morse-Zeichen
MORSE_CODE_DICT = {
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

# Umkehr-Dictionary für Decoding
MORSE_TO_TEXT = {v: k for k, v in MORSE_CODE_DICT.items()}

# JSON-Datei
HISTORY_FILE = Path("morse_history.json")


# Funktion: Text zu Morse
def encode_to_morse(text):
    text = text.upper()
    morse = " ".join(MORSE_CODE_DICT.get(ch, "") for ch in text)
    save_to_json(
        {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "input_text": text,
            "output_morse": morse,
        }
    )
    return morse


# Funktion: Morse zu Text (mit Fehlerhandling)
def decode_from_morse(morse_code):
    words = morse_code.strip().split(" ")
    decoded_chars = []

    for code in words:
        if code in MORSE_TO_TEXT:
            decoded_chars.append(MORSE_TO_TEXT[code])
        else:
            print(f"⚠ Fehler: '{code}' ist kein gültiger Morse-Code!")
            return None  # Abbrechen, wenn ein ungültiger Code auftaucht

    text = "".join(decoded_chars)

    save_to_json(
        {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "input_morse": morse_code,
            "output_text": text,
        }
    )
    return text


# Speichern in JSON
def save_to_json(entry):
    data = []
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    data.append(entry)

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main():
    while True:
        choice = input(
            "\nDeine Wahl (1=Text->Morse, 2=Morse->Text, q=Beenden): "
        ).strip()

        if not choice:  # Leere Eingabe ignorieren
            continue

        if choice == "1":
            text = input("Gib den Text ein: ").strip()
            if text:
                morse = encode_to_morse(text)
                print("➡ Morse Code:", morse)
            else:
                print("Bitte Text eingeben!")
                # FIXME jump back to pre selected input

        elif choice == "2":
            morse = input(
                "Gib den Morse Code ein (Leerzeichen trennen, '/' für Wortabstand): "
            ).strip()
            if morse:
                text = decode_from_morse(morse)
                if text:
                    print("➡ Text:", text)
            else:
                print("Bitte Morse-Code eingeben!")
                # FIXME jump back to pre selected input

        elif choice.lower() == "q":
            print("Programm beendet.")
            break

        else:
            print("Ungültige Eingabe, bitte nochmal.")


if __name__ == "__main__":
    main()
