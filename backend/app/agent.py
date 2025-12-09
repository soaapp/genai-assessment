import datetime
from .tools import AGENT_TOOLS

def run_agent(task):
    trace = [f"Agent: Received task '{task}'"]
    
    selected_tool = None
    final_output = None

    for tool_func in AGENT_TOOLS:
        result = tool_func(task, trace)
        if result:
            selected_tool, final_output = result
            break

    trace.append(f"Agent: Final Output -> '{final_output}'")

    return {
        "task": task, 
        "output": final_output, 
        "tool": selected_tool, 
        "steps": trace,
        "ts": datetime.datetime.now().isoformat()
    }
