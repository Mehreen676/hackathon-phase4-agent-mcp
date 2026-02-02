from sqlmodel import Session, select

from app.models import Conversation, Message


def get_or_create_conversation(
    session: Session,
    user_id: str,
    conversation_id: int | None,
) -> Conversation:
    if conversation_id is not None:
        convo = session.get(Conversation, conversation_id)
        if convo and convo.user_id == user_id:
            return convo

    convo = Conversation(user_id=user_id)
    session.add(convo)
    session.commit()
    session.refresh(convo)
    return convo


def save_message(
    session: Session,
    *,
    conversation_id: int,
    user_id: str,
    role: str,
    content: str,
) -> Message:
    msg = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
    )
    session.add(msg)
    session.commit()
    session.refresh(msg)
    return msg


def load_history(
    session: Session,
    *,
    conversation_id: int,
    limit: int = 12,
) -> list[Message]:
    stmt = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    rows = session.exec(stmt).all()
    return list(reversed(rows))  # oldest → newest
