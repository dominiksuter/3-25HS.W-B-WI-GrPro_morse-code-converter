# 🆘 Morse Code De-/Encoder (Console)

This project is intended to:

* Practice the complete process from **problem analysis to implementation**
* Apply basic **Python** programming concepts learned in the Programming Foundations module
* Demonstrate the use of **console interaction, data validation, and file processing**
* Produce clean, well-structured, and documented code
* Prepare students for **teamwork and documentation** in later modules
* Use this repository as a starting point by importing it into your own GitHub account.
* Work only within your own copy — do not push to the original template.
* Commit regularly to track your progress.

---

# 📖 Documentation

## 📝 Analysis

**Problem**
People are curious about Morse code, but manually encoding and decoding messages is error-prone and tedious. There’s a need for a simple tool that translates between text and Morse code quickly and reliably.

**Scenario**
A user wants to encode messages into Morse code to practice or send signals, or decode received Morse code messages. They use this application in a console, inputting either plain text, Morse code, or a text file, and receive the corresponding translation instantly. The program also keeps a history of conversions for reference.

**User stories:**

1. As a user, I want to enter text and receive the Morse code translation.
2. As a user, I want to enter Morse code and get the corresponding text.
3. As a user, I want to see error messages if I input invalid Morse code or unsupported characters.
4. As a user, I want to be able to encode or decode the contents of `.txt` files directly.
5. As a user, I want to see error messages if I input unsupported or invalid files.
6. As a user, I want all conversions to be saved automatically in a JSON history file.

**Use cases:**

* Encode text to Morse code
* Decode Morse code to text
* Process text files (`.txt`) for batch conversion
* Save conversion history to `morse_history.json`
* Display meaningful error messages for invalid input using colored console output

---

## ✅ Project Requirements

Each app must meet the following three criteria in order to be accepted:

1. Interactive app (console input)
2. Data validation (input checking)
3. File processing (read/write)

---

### 1. Interactive App (Console Input)

The application interacts with the user via the console. Users can:

* Choose to encode text to Morse code, decode Morse code to text, or process file contents
* Input text, Morse code, or a path to a `.txt` file
* View the translation immediately in the console
* Exit the program

```python
print("\nBitte wähle eine Option:")
print("1 = Text ➝  Morse")
print("2 = Morse ➝  Text")
print("3 = File Content ➝  Text / Morse")
print("q = Beenden")
```

Invalid inputs in any mode will **prompt the user again** without returning to the main menu. After an option finishes executing, the program returns to the main menu for further use. Errors are highlighted in **red** in the console using ANSI escape codes.

---

### 2. Data Validation

The application validates all user input to ensure correctness:

* **Menu validation:** Ensures only valid menu options are accepted.
* **Empty input handling:** Empty inputs are ignored and the user is prompted again.
* **Character validation:** Checks if each character or Morse code sequence is valid.
* **File validation:** Verifies that the file exists and has the correct file extension and size.

Example:

```python
if not text:
    print_error("Bitte Text eingeben!")
```

```python
if char not in TO_MORSE_DICT:
    print_error(f"Fehler: '{char}' kann nicht in Morse-Code dargestellt werden!")
```

```python
if not file_name.endswith(".txt"):
    print_error("Nur .txt-Dateien sind erlaubt!")
```

Invalid Morse sequences and unsupported characters are flagged, preventing crashes or incorrect translations.
Words in Morse code are correctly interpreted using `/` as word separator.

---

### 3. File Processing

The program supports reading and writing `.txt` files:

* Users can provide a text file to **encode to Morse** or **decode from Morse**.
* In addition to showing the translation in the console, the program automatically generates output files using the suffixes `_morse.txt` or `_text.txt` in the source file’s directory (`message.txt` → `message_morse.txt` or `message_text.txt`).

The program also maintains a **JSON conversion history** for successful translations:

* `morse_history.json` stores all sucessful translations with input, output and timestamp.
* Handles corrupted JSON files gracefully by initializing an empty list.

Example:

```json
[
    {
        "input": "HELLO WORLD",
        "output": ".... . .-.. .-.. --- / .-- --- .-. .-.. -..",
        "timestamp": "2025-11-08T14:57:17"
    }
]
```

---

## ⚙️ Implementation

### Technology

* Python 3.8+
* No external libraries required, uses only the Python standard library.
* Environment: Any IDE or terminal

**Note:** The ANSI escape codes `\033[` used for colored errors may not render correctly in all consoles. Modern terminals like Windows Terminal, PowerShell, macOS Terminal, and Linux terminals generally support them, while older `cmd.exe` may not.


### 📂 Repository Structure

```text
3-25HS.W-B-WI-GrPro_morse-code-converter/
├── .gitignore              # files git should ignore
├── main.py                 # main program logic (console application)
├── morse_history.json      # JSON file storing conversion history
└── README.md               # project description and documentation
```

### How to Run

1. Verify Python is installed with a supported version. If needed, follow the official Python documentation for installation:
```bash
python3 --version
```
2. Clone the repository:
```bash
git clone https://github.com/dominiksuter/3-25HS.W-B-WI-GrPro_morse-code-converter.git
```
3. Open the repository in your IDE or terminal.
4. Run the program:
```bash
python3 main.py
```
5. Follow the on-screen prompts to encode or decode text, Morse code, and file contents.

### Libraries Used

* `json`: For reading and writing the conversion history
* `pathlib`: For handling file paths
* `datetime`: For adding timestamps to each conversion entry

---

## 👥 Team & Contributions

| Name          | Contribution                                                                              |
| ------------- | ----------------------------------------------------------------------------------------- |
| Janis Huser   | Implemented file content translation & corresponding error handling                       |
| Fabian Jäggi  | Implemented Text-to-Morse encoding, Morse-to-Text decoding & corresponding error handling |
| Dominik Suter | Implemented user prompting, history functionality & code enhancements                     |

---

## 🧩 Example Session

```text
Bitte wähle eine Option:
1 = Text ➝  Morse
2 = Morse ➝  Text
3 = File Content ➝  Text / Morse
q = Beenden

Deine Wahl: 1
Gib den Text ein: SOS
Morse Code: ... --- ...

Deine Wahl: 2
Gib den Morse Code ein: ... --- ...
Text: SOS

Deine Wahl: 3
Dateiname eingeben (nur .txt Files möglich): message.txt
1 = Text ➝ Morse, 2 = Morse ➝ Text: 1
Morse-Code gespeichert in: message_morse.txt
```

---

## 📝 License

This project is provided for **educational use only** as part of the Programming Foundations module.
[MIT License](LICENSE)