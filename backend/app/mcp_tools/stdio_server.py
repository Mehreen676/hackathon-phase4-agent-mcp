# backend/app/mcp_tools/stdio_server.py

from mcp.server.fastmcp import FastMCP
from sqlmodel import Session, select

from app.database import engine
from app.models import Task

mcp = FastMCP("todo-mcp-server")


@mcp.tool()
def add_task(user_id: str, title: str) -> str:
    """Add a new task"""
    with Session(engine) as session:
        task = Task(user_id=user_id, title=title, completed=False)
        session.add(task)
        session.commit()
        return f"Task added: {title}"


@mcp.tool()
def list_tasks(user_id: str) -> str:
    """List all tasks"""
    with Session(engine) as session:
        tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        if not tasks:
            return "No tasks found."
        return "\n".join([f"- {t.title} ({'done' if t.completed else 'pending'})" for t in tasks])


@mcp.tool()
def complete_task(user_id: str, title: str) -> str:
    """Mark task as completed (by exact title)"""
    with Session(engine) as session:
        task = session.exec(
            select(Task).where(Task.user_id == user_id).where(Task.title == title)
        ).first()
        if not task:
            return "Task not found."
        task.completed = True
        session.add(task)
        session.commit()
        return f"Task completed: {title}"


@mcp.tool()
def delete_task(user_id: str, title: str) -> str:
    """Delete a task (by exact title)"""
    with Session(engine) as session:
        task = session.exec(
            select(Task).where(Task.user_id == user_id).where(Task.title == title)
        ).first()
        if not task:
            return "Task not found."
        session.delete(task)
        session.commit()
        return f"Task deleted: {title}"


@mcp.tool()
def update_task(user_id: str, old_title: str, new_title: str) -> str:
    """Update task title"""
    with Session(engine) as session:
        task = session.exec(
            select(Task).where(Task.user_id == user_id).where(Task.title == old_title)
        ).first()
        if not task:
            return "Task not found."
        task.title = new_title
        session.add(task)
        session.commit()
        return f"Task updated: {new_title}"


def main() -> None:
    # STDIO transport (Agents SDK connects via MCPServerStdio)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
