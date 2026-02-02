import os
from openai import OpenAI

from app.mcp_tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task,
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_agent():
    """
    Phase-3 Agent placeholder.
    Next step me is agent ko chat router se connect karenge
    aur MCP tools bind karenge.
    """
    return client
