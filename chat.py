from database import session, Chat, Message


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


def delete_chat(chat_id):
    chat_to_delete = session.get(Chat, chat_id)
    if chat_to_delete:
        session.delete(chat_to_delete)
        session.commit()
