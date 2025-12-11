import json
from pathlib import Path
from datetime import datetime

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
"""
Lookup dictionary for encoding text to Morse code.
Keys are characters, values are Morse code representations.
"""
TO_TEXT_DICT = {v: k for k, v in TO_MORSE_DICT.items()}
"""
Lookup dictionary for decoding Morse code to text.
Keys are Morse code representations, values are characters.
"""
HISTORY_FILE = Path("morse_history.json")
"""
Path to the JSON file where conversion history is stored.
"""
MAX_FILE_SIZE_MEGABYTES = 1
"""
Maximum allowed file size for input files in megabytes.
"""
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MEGABYTES * 1024 * 1024
"""
Maximum allowed file size for input files in bytes.
"""


def is_morse(content):
    """
    Checks if the given content is valid Morse code by verifying that it only contains
    the allowed characters.
    """
    allowed_chars = set(".-/ ")
    return all(c in allowed_chars for c in content)


def encode(text):
    """
    Encode the given text to Morse code.
    The operation is logged as an entry to a JSON file.
    """
    text = text.upper()
    encoded_chars = []

    for char in text:
        if char in TO_MORSE_DICT:
            encoded_chars.append(TO_MORSE_DICT[char])
        else:
            printError(f"Fehler: '{char}' kann nicht in Morse-Code dargestellt werden!")
            return None

    morse_code = " ".join(encoded_chars)
    save_to_json(text, morse_code)
    return morse_code


def decode(morse_code):
    """
    Decode the given Morse code to text.
    The operation is logged as an entry to a JSON file.
    """
    words = morse_code.strip().split(" ")
    decoded_chars = []

    for code in words:
        if code in TO_TEXT_DICT:
            decoded_chars.append(TO_TEXT_DICT[code])
        else:
            printError(f"Fehler: '{code}' ist kein gültiger Morse-Buchstabe!")
            return None

    text = "".join(decoded_chars)
    save_to_json(morse_code, text)
    return text


def save_to_json(input, output):
    """
    Save the given entry to the JSON history file.
    """
    data = []
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []

    data.append(
        {
            "input": input,
            "output": output,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }
    )

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def printError(message):
    """
    Print the given message in red color to indicate an error.
    """
    # \033[ starts the escape sequence
    # 31m sets the text color to red
    # \033[0m resets the text formatting
    print(f"\033[31m{message}\033[0m")


def handleTextToMorse():
    """
    Handle user input for Text to Morse code conversion.
    """
    while True:
        text = input("Gib den Text ein: ").strip()
        if not text:
            printError("Bitte Text eingeben!")
            continue
        if morse := encode(text):
            print("Morse Code:", morse)
        break


def handleMorseToText():
    """
    Handle user input for Morse code to Text conversion.
    """
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
    """
    Handle user input for file content conversion between Text and Morse code.
    """
    while True:
        file_name = input("Dateiname eingeben (nur .txt Files möglich): ").strip()
        if not file_name:
            printError("Bitte Dateiname eingeben!")
            continue

        if not file_name.endswith(".txt"):
            printError("Nur .txt-Dateien sind erlaubt!")
            continue

        file_path = Path(file_name)
        if not file_path.exists() or not file_path.is_file():
            printError("Datei existiert nicht!")
            continue

        file_size = file_path.stat().st_size
        if file_size > MAX_FILE_SIZE_BYTES:
            printError(
                f"Datei ist zu gross ({file_size / (1024 * 1024):.2f} MB). Maximal erlaubt: {MAX_FILE_SIZE_MEGABYTES} MB."
            )
            continue

        direction = input("1 = Text ➝ Morse, 2 = Morse ➝ Text: ").strip()
        if direction not in ["1", "2"]:
            printError("Ungültige Wahl, bitte 1 oder 2 eingeben!")
            continue

        with open(file_name, "r", encoding="utf-8") as f:
            content = f.read().strip()

        while True:
            if direction == "1":
                if is_morse(content):
                    print("Warnung: Datei scheint bereits Morse-Code zu sein!")
                else:
                    morse = encode(content)
                    if morse:
                        print("Morse Code:\n", morse)
                        out_file = file_name.replace(".txt", "_morse.txt")
                        with open(out_file, "w", encoding="utf-8") as f:
                            f.write(morse)
                        print(f"Morse-Code gespeichert in: {out_file}")
                break
            elif direction == "2":
                text = decode(content)
                if text:
                    print("Text:\n", text)
                    out_file = file_name.replace(".txt", "_text.txt")
                    with open(out_file, "w", encoding="utf-8") as f:
                        f.write(text)
                    print(f"Text gespeichert in: {out_file}")
                break
        break


def main():
    """
    Main function to interact with the user.
    """
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
    except Exception as e:
        printError(f"Ein unerwarteter Fehler ist aufgetreten: {e}")


if __name__ == "__main__":
    main()
