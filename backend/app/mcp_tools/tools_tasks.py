from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime

from app.models import Task


# MCP TOOL: add_task
def add_task(
    session: Session,
    user_id: str,
    title: str,
    description: Optional[str] = None,
) -> Task:
    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# MCP TOOL: list_tasks
def list_tasks(session: Session, user_id: str) -> List[Task]:
    stmt = select(Task).where(Task.user_id == user_id).order_by(Task.id)
    return session.exec(stmt).all()


# MCP TOOL: complete_task
def complete_task(session: Session, user_id: str, task_id: int) -> Task:
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise ValueError("Task not found")

    task.completed = True
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# MCP TOOL: delete_task
def delete_task(session: Session, user_id: str, task_id: int) -> None:
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise ValueError("Task not found")

    session.delete(task)
    session.commit()


# MCP TOOL: update_task
def update_task(
    session: Session,
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> Task:
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise ValueError("Task not found")

    if title is not None:
        task.title = title
    if description is not None:
        task.description = description

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

