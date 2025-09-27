# Morse Code Converter (for 3-25HS.W-B-WI-GrPro)

A simple command-line tool to **encode text into Morse code** and **decode Morse code back into text**.  
All conversions are saved to a local JSON file (`morse_history.json`) with timestamps for later reference.

---

## ✨ Features
- 🔤 Encode plain text to Morse code
- 📡 Decode Morse code to plain text
- ⚠ Error handling for invalid Morse sequences
- 📝 Automatic history logging in JSON format
- ⌚ Timestamped entries for better tracking

---

## 📂 Project Structure
```
.
├── morse_converter.py   # Main script
├── morse_history.json   # Conversion history (auto-generated)
└── README.md            # Documentation
```

---

## ▶️ Usage

### 1. Run the program
```bash
python morse_converter.py
```

### 2. Choose an option in the menu
- **1** → Text ➝ Morse  
- **2** → Morse ➝ Text  
- **q** → Quit the program  

---

## 💡 Examples

### Encode text
```
Deine Wahl (1=Text->Morse, 2=Morse->Text, q=Beenden): 1
Gib den Text ein: SOS
➡ Morse Code: ... --- ...
```

### Decode Morse
```
Deine Wahl (1=Text->Morse, 2=Morse->Text, q=Beenden): 2
Gib den Morse Code ein (Leerzeichen trennen, '/' für Wortabstand): ... --- ...
➡ Text: SOS
```

---

## 🗂 History Logging
Each conversion is saved in `morse_history.json`:
```json
[
    {
        "timestamp": "2025-09-27T14:32:10",
        "input_text": "HELLO",
        "output_morse": ".... . .-.. .-.. ---"
    },
    {
        "timestamp": "2025-09-27T14:33:05",
        "input_morse": "... --- ...",
        "output_text": "SOS"
    }
]
```

---

## ⚙️ Requirements
- Python **3.7+**
- No external libraries required (only uses standard library)

---

## 🚀 Future Ideas
- Add support for saving history in **CSV** or **SQLite**
- Build a simple **GUI version**
- Play Morse code sounds for better learning

---

## 📜 License
This project is licensed under the MIT License – feel free to use and modify it.
