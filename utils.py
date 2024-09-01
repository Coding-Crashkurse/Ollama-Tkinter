# utils.py
import socket
import webbrowser
import subprocess
from tkinter import messagebox
from database import session, User, Chat, Message
from sqlalchemy.orm import sessionmaker
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

# Initialize ChatOllama LLM
llm = ChatOllama(
    model="llama3.1",
    temperature=0,
)


# Functionality
def register_user(username, password):
    if session.query(User).filter_by(username=username).first():
        return False
    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()
    return True


def login_user(username, password):
    return session.query(User).filter_by(username=username, password=password).first()


def create_chat(user_id, chat_name):
    new_chat = Chat(chat_name=chat_name, user_id=user_id)
    session.add(new_chat)
    session.commit()
    return new_chat


def get_user_chats(user_id):
    return session.query(Chat).filter_by(user_id=user_id).all()


def save_message(chat_id, content):
    new_message = Message(content=content, chat_id=chat_id)
    session.add(new_message)
    session.commit()


def get_chat_messages(chat_id):
    return session.query(Message).filter_by(chat_id=chat_id).all()


# Ollama management
def is_ollama_running():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("localhost", 11434))
    sock.close()
    return result == 0


def download_ollama():
    url = "https://ollama.com/download/OllamaSetup.exe"
    webbrowser.open(url)


def prompt_for_ollama():
    if not is_ollama_running():
        answer = messagebox.askyesno(
            "Ollama Not Detected",
            "Ollama is not running on port 11434. Would you like to download it?",
        )
        if answer:
            download_ollama()


def manage_model(action, model_name):
    command = f"ollama {action} {model_name}"
    try:
        subprocess.run(command, shell=True, check=True)
        messagebox.showinfo(
            "Success", f"{action.capitalize()} {model_name} successfully!"
        )
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", f"Failed to {action} {model_name}.")
