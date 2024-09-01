# ui.py
import customtkinter as ctk
from tkinter import messagebox
from threading import Thread
from utils import *


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x600")
        self.root.title("Chat Application")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.current_user = None
        self.current_chat = None

        # Initialize frames
        self.login_frame = LoginFrame(self)
        self.register_frame = RegisterFrame(self)
        self.chat_frame = ChatFrame(self)
        self.model_manager_frame = ModelManagerFrame(self)

        # Start the application
        self.on_start()

    def on_start(self):
        prompt_for_ollama()
        self.login_frame.show()

    def switch_to_frame(self, frame):
        self.login_frame.hide()
        self.register_frame.hide()
        self.chat_frame.hide()
        self.model_manager_frame.hide()
        frame.show()

    def run(self):
        self.root.mainloop()


class LoginFrame:
    def __init__(self, app):
        self.app = app
        self.frame = ctk.CTkFrame(app.root)

        ctk.CTkLabel(self.frame, text="Login").pack(pady=12)
        self.entry_username = ctk.CTkEntry(self.frame, placeholder_text="Username")
        self.entry_username.pack(pady=5)
        self.entry_password = ctk.CTkEntry(
            self.frame, placeholder_text="Password", show="*"
        )
        self.entry_password.pack(pady=5)
        ctk.CTkButton(self.frame, text="Login", command=self.handle_login).pack(pady=20)
        ctk.CTkButton(
            self.frame, text="Register", command=self.show_register_frame
        ).pack()
        ctk.CTkButton(
            self.frame, text="Manage Models", command=self.show_model_manager
        ).pack(pady=5)

    def show(self):
        self.frame.pack(pady=20)

    def hide(self):
        self.frame.pack_forget()

    def handle_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        user = login_user(username, password)
        if user:
            messagebox.showinfo("Success", "Login successful!")
            self.app.current_user = user
            self.app.switch_to_frame(self.app.chat_frame)
        else:
            messagebox.showerror("Error", "Invalid login credentials.")

    def show_register_frame(self):
        self.app.switch_to_frame(self.app.register_frame)

    def show_model_manager(self):
        self.app.switch_to_frame(self.app.model_manager_frame)


class RegisterFrame:
    def __init__(self, app):
        self.app = app
        self.frame = ctk.CTkFrame(app.root)

        ctk.CTkLabel(self.frame, text="Register").pack(pady=12)
        self.entry_username = ctk.CTkEntry(self.frame, placeholder_text="Username")
        self.entry_username.pack(pady=5)
        self.entry_password = ctk.CTkEntry(
            self.frame, placeholder_text="Password", show="*"
        )
        self.entry_password.pack(pady=5)
        ctk.CTkButton(self.frame, text="Register", command=self.handle_register).pack(
            pady=20
        )
        ctk.CTkButton(
            self.frame, text="Back to Login", command=self.show_login_frame
        ).pack()

    def show(self):
        self.frame.pack(pady=20)

    def hide(self):
        self.frame.pack_forget()

    def handle_register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if register_user(username, password):
            messagebox.showinfo("Success", "Registration successful!")
            self.show_login_frame()
        else:
            messagebox.showerror("Error", "Username already exists.")

    def show_login_frame(self):
        self.app.switch_to_frame(self.app.login_frame)


class ChatFrame:
    def __init__(self, app):
        self.app = app
        self.frame = ctk.CTkFrame(app.root)

        self.chat_list_frame = ctk.CTkFrame(self.frame, width=200, corner_radius=0)
        self.chat_list_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.chat_display_frame = ctk.CTkFrame(self.frame)
        self.chat_display_frame.pack(
            side="right", fill="both", expand=True, padx=10, pady=10
        )

        self.chat_display = ctk.CTkTextbox(
            self.chat_display_frame, state="disabled", height=400
        )
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=10)

        self.entry_message = ctk.CTkEntry(
            self.chat_display_frame, placeholder_text="Enter your message..."
        )
        self.entry_message.pack(pady=5, fill="x", padx=10)

        self.send_button = ctk.CTkButton(
            self.chat_display_frame, text="Send", command=self.send_message
        )
        self.send_button.pack(pady=5)

        self.entry_new_chat = ctk.CTkEntry(
            self.chat_list_frame, placeholder_text="New Chat Name"
        )
        self.entry_new_chat.pack(pady=5, fill="x", padx=20)

        self.create_chat_button = ctk.CTkButton(
            self.chat_list_frame, text="New Chat", command=self.create_new_chat
        )
        self.create_chat_button.pack(pady=5, padx=20, fill="x")

    def show(self):
        self.frame.pack(pady=20, fill="both", expand=True)
        self.load_chats(self.app.current_user)

    def hide(self):
        self.frame.pack_forget()

    def load_chats(self, user):
        chats = get_user_chats(user.id)
        for chat in chats:
            self.add_chat_button(chat.chat_name, chat.id)

    def add_chat_button(self, chat_name, chat_id):
        chat_frame = ctk.CTkFrame(self.chat_list_frame)
        chat_frame.pack(pady=5, padx=20, fill="x")

        chat_button = ctk.CTkButton(
            chat_frame,
            text=chat_name,
            anchor="w",
            command=lambda: self.load_chat_messages(chat_id),
        )
        chat_button.pack(side="left", fill="x", expand=True)

        delete_button = ctk.CTkButton(
            chat_frame,
            text="x",
            width=30,
            command=lambda: self.delete_chat(chat_id, chat_frame),
        )
        delete_button.pack(side="right", padx=5)

    def delete_chat(self, chat_id, chat_frame):
        chat_to_delete = session.get(Chat, chat_id)
        if chat_to_delete:
            session.delete(chat_to_delete)
            session.commit()

        chat_frame.pack_forget()
        chat_frame.destroy()

    def create_new_chat(self):
        chat_name = self.entry_new_chat.get()
        if chat_name and self.app.current_user:
            chat = create_chat(self.app.current_user.id, chat_name)
            self.add_chat_button(chat.chat_name, chat.id)
            self.entry_new_chat.delete(0, "end")

    def load_chat_messages(self, chat_id):
        self.app.current_chat = chat_id
        self.chat_display.configure(state="normal")
        self.chat_display.delete(1.0, "end")
        messages = get_chat_messages(chat_id)
        for message in messages:
            self.chat_display.insert("end", f"{message.content}\n")
        self.chat_display.configure(state="disabled")

    def send_message(self):
        message = self.entry_message.get()
        if message and self.app.current_chat:
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", f"You: {message}\n")
            self.chat_display.see("end")
            save_message(self.app.current_chat, f"You: {message}")

            messages = [
                SystemMessage(content="You are a helpful assistant."),
                HumanMessage(content=message),
            ]

            self.chat_display.insert("end", "AI: ")
            for chunk in llm.stream(messages):
                self.chat_display.insert("end", chunk.content)
                self.chat_display.see("end")
                self.chat_display.update_idletasks()

            self.chat_display.insert("end", "\n")
            self.chat_display.configure(state="disabled")

            ai_content = "".join([chunk.content for chunk in llm.stream(messages)])
            save_message(self.app.current_chat, f"AI: {ai_content}")
            self.entry_message.delete(0, "end")


class ModelManagerFrame:
    def __init__(self, app):
        self.app = app
        self.frame = ctk.CTkFrame(app.root)

        ctk.CTkLabel(self.frame, text="Model Manager").pack(pady=12)
        models = ["mistral-nemo", "llama3.1", "phi3.5"]

        for model in models:
            ctk.CTkButton(
                self.frame,
                text=f"Pull {model}",
                command=lambda m=model: manage_model("pull", m),
            ).pack(pady=5)

            ctk.CTkButton(
                self.frame,
                text=f"Remove {model}",
                command=lambda m=model: manage_model("rm", m),
            ).pack(pady=5)

        ctk.CTkButton(
            self.frame, text="Back to Login", command=self.show_login_frame
        ).pack(pady=20)

    def show(self):
        self.frame.pack(pady=20, fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()

    def show_login_frame(self):
        self.app.switch_to_frame(self.app.login_frame)
