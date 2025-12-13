"""Core agent logic that routes tasks to appropriate tools"""

import datetime
from .tools import AGENT_TOOLS

def run_agent(task):
    """Execute a task by selecting and running the first matching tool."""
    trace = [f"Agent: Received task '{task}'"]

    selected_tool = None
    final_output = None

    # Try each tool until one returns a result. (There is no LLM so this would be agent "intelligently" picking a tool.)
    for tool_func in AGENT_TOOLS:
        result = tool_func(task, trace)
        if result:
            selected_tool, final_output = result
            break

    trace.append(f"Agent: Final Output -> '{final_output}'")

    # Add step numbers to all trace entries
    numbered_trace = [f"Step {i}: {entry}" for i, entry in enumerate(trace, 1)]

    return {
        "task": task,
        "output": final_output,
        "tool": selected_tool,
        "steps": numbered_trace,
        "ts": datetime.datetime.now().isoformat()
    }
