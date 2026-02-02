from typing import Optional, List, Dict
from sqlmodel import Session, select

from app.models import Conversation, Message

def get_or_create_conversation(session: Session, user_id: str) -> Conversation:
    convo = session.exec(
        select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.id.desc())
    ).first()

    if convo:
        return convo

    convo = Conversation(user_id=user_id)
    session.add(convo)
    session.commit()
    session.refresh(convo)
    return convo

def load_history(session: Session, conversation_id: int, limit: int = 50) -> List[Dict[str, str]]:
    msgs = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.id.asc())
        .limit(limit)
    ).all()

    return [{"role": m.role, "content": m.content} for m in msgs]

def save_message(session: Session, conversation_id: int, role: str, content: str) -> Message:
    msg = Message(conversation_id=conversation_id, role=role, content=content)
    session.add(msg)
    session.commit()
    session.refresh(msg)
    return msg
