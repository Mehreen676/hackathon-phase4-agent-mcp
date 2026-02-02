from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session, select
from datetime import datetime

from app.db import get_session
from app.models import Task
from app.schemas import TaskCreate, TaskRead

router = APIRouter()


@router.get("/{user_id}/tasks", response_model=List[TaskRead])
@router.get("/{user_id}/tasks/", response_model=List[TaskRead])
def list_tasks(user_id: str, session: Session = Depends(get_session)):
    stmt = select(Task).where(Task.user_id == user_id).order_by(Task.id)
    return session.exec(stmt).all()


@router.post("/{user_id}/tasks", response_model=TaskRead)
@router.post("/{user_id}/tasks/", response_model=TaskRead)
def create_task(
    user_id: str,
    payload: TaskCreate,
    session: Session = Depends(get_session),
):
    task = Task(
        user_id=user_id,
        title=payload.title,
        description=payload.description,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# 🔥 IMPORTANT FIX: allow BOTH with and without trailing slash
@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskRead)
@router.patch("/{user_id}/tasks/{task_id}/complete/", response_model=TaskRead)
def toggle_complete(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
):
    stmt = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id,
    )
    task = session.exec(stmt).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{user_id}/tasks/{task_id}")
@router.delete("/{user_id}/tasks/{task_id}/")
def delete_task(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
):
    stmt = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id,
    )
    task = session.exec(stmt).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"ok": True}
