# backend/app/mcp_tools/tools.py
from __future__ import annotations

from datetime import datetime
from typing import Optional, Dict, Any, List

from sqlmodel import Session, select

from app.database import engine
from app.models import Task


def _to_task_dict(t: Task) -> Dict[str, Any]:
    return {
        "id": t.id,
        "user_id": t.user_id,
        "title": t.title,
        "description": getattr(t, "description", None),
        "completed": t.completed,
        "created_at": getattr(t, "created_at", None),
        "updated_at": getattr(t, "updated_at", None),
    }


def register_tools(mcp) -> None:
    """
    IMPORTANT:
    - Ye tools SAME DB (engine) + SAME Task model use karte hain jo /tasks router use karta hai.
    - list_tasks MUST ids return kare, warna agent wrong id pick karega.
    """

    @mcp.tool()
    def add_task(user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        title = (title or "").strip()
        if not title:
            return {"ok": False, "error": "title is required"}

        now = datetime.utcnow()

        with Session(engine) as session:
            task = Task(
                user_id=user_id,
                title=title,
                description=description,
                completed=False,
                created_at=now,
                updated_at=now,
            )
            session.add(task)
            session.commit()
            session.refresh(task)

            return {"ok": True, "task": _to_task_dict(task)}

    @mcp.tool()
    def list_tasks(user_id: str, status: Optional[str] = None) -> Dict[str, Any]:
        """
        status: optional -> "pending" | "completed" | None
        """
        with Session(engine) as session:
            stmt = select(Task).where(Task.user_id == user_id).order_by(Task.id)

            rows = session.exec(stmt).all()

            if status:
                s = status.lower().strip()
                if s in ("pending", "incomplete", "open"):
                    rows = [t for t in rows if not t.completed]
                elif s in ("completed", "done", "closed"):
                    rows = [t for t in rows if t.completed]

            return {"ok": True, "tasks": [_to_task_dict(t) for t in rows]}

    @mcp.tool()
    def complete_task(user_id: str, task_id: int) -> Dict[str, Any]:
        with Session(engine) as session:
            task = session.get(Task, task_id)
            if not task or task.user_id != user_id:
                return {"ok": False, "error": f"Task id {task_id} not found"}

            task.completed = True
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)

            return {"ok": True, "task": _to_task_dict(task)}

    @mcp.tool()
    def delete_task(user_id: str, task_id: int) -> Dict[str, Any]:
        with Session(engine) as session:
            task = session.get(Task, task_id)
            if not task or task.user_id != user_id:
                return {"ok": False, "error": f"Task id {task_id} not found"}

            session.delete(task)
            session.commit()
            return {"ok": True}

    @mcp.tool()
    def update_task(
        user_id: str,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        with Session(engine) as session:
            task = session.get(Task, task_id)
            if not task or task.user_id != user_id:
                return {"ok": False, "error": f"Task id {task_id} not found"}

            if title is not None:
                task.title = title.strip()
            if description is not None:
                task.description = description

            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)

            return {"ok": True, "task": _to_task_dict(task)}
