# backend/app/agent_runner.py
import os
from datetime import datetime
from typing import Optional, List, Dict, Any

from agents import Agent, Runner, set_default_openai_api
from agents.mcp import MCPServerStdio

from sqlmodel import Session, select
from app.database import engine
from app.models import Conversation, Message


SYSTEM_INSTRUCTIONS = """
You are a Todo Chatbot.
You MUST manage tasks ONLY by calling MCP tools.

CRITICAL:
- NEVER ask for user_id. USER_ID is provided in the prompt as: USER_ID: <value>

MCP tools:
- add_task(user_id, title, description?)
- list_tasks(user_id, status?)
- complete_task(user_id, task_id)
- delete_task(user_id, task_id)
- update_task(user_id, task_id, title?, description?)

IMPORTANT RULES:
- When you list tasks, ALWAYS show task IDs in your response.
- For complete/delete/update, ALWAYS use the numeric task_id (never guess by title).
- If the user gives a title/name instead of an ID, first call list_tasks and ask which ID to use.

Return short helpful confirmations.
""".strip()


def _get_or_create_conversation(user_id: str, conversation_id: Optional[int] = None) -> int:
    with Session(engine) as session:
        if conversation_id is not None:
            convo = session.get(Conversation, conversation_id)
            if convo and convo.user_id == user_id:
                return convo.id

        convo = session.exec(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.id.desc())
        ).first()

        if convo:
            return convo.id

        convo = Conversation(user_id=user_id)
        session.add(convo)
        session.commit()
        session.refresh(convo)
        return convo.id


def _load_history(conversation_id: int, limit: int = 30) -> List[Dict[str, str]]:
    """
    Return last N messages in chronological order.
    Ensures roles are normalized for the agent prompt.
    """
    with Session(engine) as session:
        # load all ids asc then slice; simple + safe
        msgs = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.id.asc())
        ).all()

    msgs = msgs[-limit:]

    out: List[Dict[str, str]] = []
    for m in msgs:
        role = (m.role or "").lower().strip()
        if role not in ("user", "assistant"):
            # fallback: treat unknown as assistant to avoid breaking context
            role = "assistant"
        out.append({"role": role, "content": m.content})
    return out


def _store_message(*, conversation_id: int, user_id: str, role: str, content: str) -> None:
    with Session(engine) as session:
        session.add(
            Message(
                conversation_id=conversation_id,
                user_id=user_id,
                role=role,
                content=content,
            )
        )
        convo = session.get(Conversation, conversation_id)
        if convo:
            convo.updated_at = datetime.utcnow()
        session.commit()


def _build_prompt(user_id: str, history: List[Dict[str, str]], user_message: str) -> str:
    lines: List[str] = [f"USER_ID: {user_id}"]

    for h in history:
        r = h["role"]
        if r == "user":
            lines.append(f"USER: {h['content']}")
        else:
            lines.append(f"ASSISTANT: {h['content']}")

    lines.append(f"USER: {user_message}")
    return "\n".join(lines)


async def run_chat(user_id: str, message: str, conversation_id: Optional[int] = None) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY missing in env")

    set_default_openai_api(api_key)

    conversation_id = _get_or_create_conversation(user_id, conversation_id)

    # history BEFORE storing new message
    history = _load_history(conversation_id)

    _store_message(conversation_id=conversation_id, user_id=user_id, role="user", content=message)

    prompt = _build_prompt(user_id, history, message)

    async with MCPServerStdio(
        name="todo-mcp",
        params={"command": "python", "args": ["-m", "app.mcp_tools.server"]},
        client_session_timeout_seconds=60,
    ) as todo_mcp:
        agent = Agent(
            name="TodoAgent",
            instructions=SYSTEM_INSTRUCTIONS,
            model=os.getenv("OPENAI_MODEL", "gpt-5"),
            mcp_servers=[todo_mcp],
        )

        result = await Runner.run(agent, prompt)
        reply_text = result.final_output or "OK"

    _store_message(conversation_id=conversation_id, user_id=user_id, role="assistant", content=reply_text)

    return {"reply": reply_text, "conversation_id": conversation_id, "tool_calls": []}
