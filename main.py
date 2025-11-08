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

# Funktion: Prüfen ob String Morse-Code ist
def is_morse(content):
    allowed_chars = set(".-/ ")
    return all(c in allowed_chars for c in content)

# Funktion: Text zu Morse
def encode(text):
    text = text.upper()
    encoded_chars = []

    for char in text:
        if char in TO_MORSE_DICT:
            encoded_chars.append(TO_MORSE_DICT[char])
        else:
            printError(f"Fehler: '{char}' kann nicht in Morse-Code dargestellt werden!")
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
            printError(f"Fehler: '{code}' ist kein gültiger Morse-Buchstabe!")
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


# Format message with red color using ANSI escape codes
def printError(message):
    # \033[ starts the escape sequence
    # 31m sets the text color to red
    # \033[0m resets the text formatting
    print(f"\033[31m{message}\033[0m")


def handleTextToMorse():    
    while True:
        text = input("Gib den Text ein: ").strip()
        if not text:
            printError("Bitte Text eingeben!")
            continue
        if morse := encode(text):
            print("Morse Code:", morse)
        break

def handleMorseToText():    
    while True:
        morse = input(
            "Gib den Morse Code ein (Morse-Buchstaben mit Leerzeichen getrennt, '/' für Wortabstand): "
        ).strip()
        if not morse:
            printError("Bitte Morse-Code eingeben!")
            continue
        if text := decode(morse):
            print("Text:", text)
            break

def handleFileContent():
    while True:
        filename = input("Dateiname eingeben (nur .txt Files möglich): ").strip()
        if not filename:
            print("Bitte Dateiname eingeben!")
            continue
        
        if not Path(filename).exists():
            print("Datei existiert nicht!")
            continue
        
        direction = input("1 = Text ➝ Morse, 2 = Morse ➝ Text: ").strip()
        if direction not in ["1", "2"]:
            print("Ungültige Wahl, bitte 1 oder 2 eingeben!")
            continue
        
        # Datei einlesen
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
        
        while True:
            if direction == "1":
                if is_morse(content):
                    print("Warnung: Datei scheint bereits Morse-Code zu sein!")
                else:
                    morse = encode(content)
                    if morse:
                        print("Morse Code:\n", morse)
                        out_file = filename.replace(".txt", "_morse.txt")
                        with open(out_file, "w", encoding="utf-8") as f:
                            f.write(morse)
                        print(f"Morse-Code gespeichert in: {out_file}")
                break
            elif direction == "2":
                text = decode(content)
                if text:
                    print("Text:\n", text)
                    out_file = filename.replace(".txt", "_text.txt")
                    with open(out_file, "w", encoding="utf-8") as f:
                        f.write(text)
                    print(f"Text gespeichert in: {out_file}")
                break
        break

# Interaktion mit User
def main():
    try:
        while True:
            print("\nBitte wähle eine Option:")
            print("1 = Text ➝  Morse")
            print("2 = Morse ➝  Text")
            print("3 = File Content ➝  Text / Morse")
            print("q = Beenden")

            choice = input("\nDeine Wahl: ").strip()

            if not choice:
                printError("Keine Eingabe, bitte nochmal.")
                continue

            if choice == "1":
                handleTextToMorse()
            elif choice == "2":
                handleMorseToText()
            elif choice == "3":
                handleFileContent()
            elif choice.lower() == "q":
                print("Programm beendet.")
                break
            else:
                printError("Ungültige Eingabe, bitte nochmal.")
    except:
        printError("Ein unerwarteter Fehler ist aufgetreten.")


# Starte das Hauptprogramm
if __name__ == "__main__":
    main()
