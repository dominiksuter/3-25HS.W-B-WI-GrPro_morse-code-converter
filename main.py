import json
from pathlib import Path
from datetime import datetime

# Dictionary mit Morse-Zeichen
TO_MORSE_DICT = {
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
TO_TEXT_DICT = {v: k for k, v in TO_MORSE_DICT.items()}

# JSON-Datei für die History
HISTORY_FILE = Path("morse_history.json")

# TODO encode and decode can be fused into one function

# Funktion: Text zu Morse
def encode(text):
    text = text.upper()
    encoded_chars = []

    for char in text:
        if char in TO_MORSE_DICT:
            encoded_chars.append(TO_MORSE_DICT[char])
        else:
            print(f"Fehler: '{char}' kann nicht in Morse-Code dargestellt werden!")
            return None

    morse_code = " ".join(TO_MORSE_DICT.get(char, "") for char in text)

    save_to_json(
        {   
            "input": text,
            "output": morse_code,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }
    )

    return morse_code


# Funktion: Morse zu Text
def decode(morse_code):
    words = morse_code.strip().split(" ")
    decoded_chars = []

    for code in words:
        if code in TO_TEXT_DICT:
            decoded_chars.append(TO_TEXT_DICT[code])
        else:
            print(f"Fehler: '{code}' ist kein gültiger Morse-Code!")
            return None

    text = "".join(decoded_chars)

    save_to_json(
        {
            "input": morse_code,
            "output": text,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }
    )
    return text


# Speichern in JSON
def save_to_json(entry):
    data = []
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []

    data.append(entry)

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# Interaktion mit User
def main():
    while True:
        print("\nBitte wähle eine Option:")
        print("1 = Text ➝  Morse")
        print("2 = Morse ➝  Text")
        print("q = Beenden")

        choice = input("\nDeine Wahl: ").strip()

        if not choice:  # Leere Eingabe ignorieren
            print("Keine Eingabe, bitte nochmal.")
            continue

        if choice == "1":
            text = input("Gib den Text ein: ").strip()
            if text:
                morse = encode(text)
                if morse:
                    print("Morse Code:", morse)
            else:
                print("Bitte Text eingeben!")
                # FIXME jump back to pre selected input


        elif choice == "2":
            morse = input(
                "Gib den Morse Code ein (Leerzeichen trennen, '/' für Wortabstand): "
            ).strip()
            if morse:
                text = decode(morse)
                if text:
                    print("Text:", text)
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
