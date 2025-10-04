# 🆘 Morse Code De-/Encoder (Console)

This project is intended to:

- Practice the complete process from **problem analysis to implementation**  
- Apply basic **Python** programming concepts learned in the Programming Foundations module  
- Demonstrate the use of **console interaction, data validation, and file processing**  
- Produce clean, well-structured, and documented code  
- Prepare students for **teamwork and documentation** in later modules  
- Use this repository as a starting point by importing it into your own GitHub account.  
- Work only within your own copy — do not push to the original template.  
- Commit regularly to track your progress.  

# 📖 Documentation

## 📝 Analysis

**Problem**  
People are curious about Morse code, but manually encoding and decoding messages is error-prone and tedious. There’s a need for a simple tool that translates between text and Morse code quickly and reliably.

**Scenario**  
A user wants to encode messages into Morse code to practice or send signals, or decode received Morse code messages. They use this application in a console, inputting either plain text or Morse code, and receive the corresponding translation instantly. The program also keeps a history of conversions for reference.

**User stories:**

1. As a user, I want to enter text and receive the Morse code translation.  
2. As a user, I want to enter Morse code and get the corresponding text.  
3. As a user, I want to see error messages if I input invalid Morse code.  
4. As a user, I want all conversions to be saved automatically in a JSON history file.  

**Use cases:**

- Encode text to Morse code  
- Decode Morse code to text  
- Save conversion history to `morse_history.json`  
- Display meaningful error messages for invalid input  

---

## ✅ Project Requirements

Each app must meet the following three criteria in order to be accepted:

1. Interactive app (console input)  
2. Data validation (input checking)  
3. File processing (read/write)  

---

### 1. Interactive App (Console Input)

The application interacts with the user via the console. Users can:  

- Choose to encode text to Morse code or decode Morse code to text  
- Input text or Morse code  
- View the translation immediately in the console  
- Exit the program gracefully  

---

### 2. Data Validation

The application validates all user input to ensure correctness:  

- **Empty input handling:** Skips processing if the user enters nothing.  

- **User input validation:** Checks each Morse code sequence or character depending on the chosen mode and prints a warning for invalid inputs.  

- **Menu choice validation:** Ensures that only valid options (1, 2, q) are processed.  

These checks prevent crashes and guide the user to provide correct input, fulfilling the validation requirement.

---

### 3. File Processing

The program reads and writes conversion history using a JSON file:  

- **Output file:** `morse_history.json` — stores a history of all conversions with timestamps, input, and output.  

- Reading the JSON file checks for existing data and prevents errors with corrupted files.

- Writing appends new entries and ensures proper formatting.  

---

## ⚙️ Implementation

### Technology

- Python 3.x  
- Environment: Any IDE or GitHub Codespaces  
- No external libraries required (only Python libraries)  

### 📂 Repository Structure

```text
3-25HS.W-B-WI-GrPro_morse-code-converter/
├── .gitignore              # files git should ignore
├── main.py                 # main program logic (console application)
├── morse_history.json      # JSON file storing conversion history
└── README.md               # project description and documentation
```

### How to Run

1. Open the repository in your IDE or terminal 
2. Run the program:  

``` 
py main.py
```  

3. Follow the on-screen prompts to encode or decode messages  

## 👥 Team & Contributions

| Name          | Contribution                                              |
| ------------- | --------------------------------------------------------- |
| Janis Huser   | Text-to-Morse encoding                                    |
| Fabian Jäggi  | Morse-to-Text decoding                                    |
| Dominik Suter | File handling, saving conversion history & error handling |

---

## 📝 License

This project is provided for **educational use only** as part of the Programming Foundations module.  
[MIT License](LICENSE)