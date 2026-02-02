from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


# =========================
# TASK MODEL (EXISTING)
# =========================
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)

    title: str
    completed: bool = Field(default=False)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# =========================
# CONVERSATION MODEL
# =========================
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# =========================
# MESSAGE MODEL
# =========================
class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(
        foreign_key="conversations.id",
        index=True
    )
    user_id: str = Field(index=True)

    role: str  # "user" | "assistant"
    content: str

    created_at: datetime = Field(default_factory=datetime.utcnow)
