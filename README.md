# Local Chat Application with Ollama Integration

This project is a fully local chat application built using `customtkinter` for the UI, integrated with Ollama's language model for generating responses. The application is standalone, meaning no web interface is needed, and everything runs locally on your machine.

## Project Structure

- **main.py**: The entry point of the application that initializes and runs the `ChatApp`.
- **ui.py**: Contains the UI logic and components, including frames for login, registration, chat, and model management.
- **database.py**: Manages the SQLAlchemy setup and defines the database models for users, chats, and messages.
- **utils.py**: Contains utility functions for user management, chat handling, and integration with Ollama's language model.
- **chat.py**: Manages chat-specific logic, possibly for handling chat messages and communication with the language model.

## How to Create an EXE File from the project

To package the application into a standalone executable, follow these steps:

1. **Install packages**:

```bash
pip install -r requirements.txt
```

2. **Install PyInstaller**:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py # single file and no console
```

3. **Run the app**:
   Navigate on the `dist` folder start the the .exe file

Of course you also just run `python main.py` :-).
