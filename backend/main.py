import sqlite3, json, re, datetime, random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def tool_calc(q, trace):
    if match := re.search(r'\d[\d\s\+\-\*\/]*', q):
        expression = match.group(0).strip()
        # Verify prompt has at least one operator
        if len(expression) > 1 and any(op in expression for op in "+-*/"):
            trace.append(f"CalculatorTool: Detected math expression '{expression}'")
            try:
                result = str(eval(expression))
                trace.append(f"CalculatorTool: Successfully evaluated '{expression}' = {result}")
                return "CalculatorTool", result
            except:
                trace.append(f"CalculatorTool: Failed to eval '{expression}'")
                pass
    return None

def tool_weather(q, trace):
    if "weather" in q.lower():
        trace.append("WeatherTool: Detected keyword 'weather'")
        
        city = "Unknown"
        for p in ["in ", "at ", "for "]:
            if p in q:
                city = q.split(p)[1].strip()
                trace.append(f"WeatherTool: Extracted location '{city}'")
                break
        
        # Randomize weather for fun
        conditions = ["Sunny", "Cloudy", "Rainy", "Snowing", "Partly Cloudy"]
        temp = random.randint(-10, 25)
        condition = random.choice(conditions)
        
        result = f"{temp}°C, {condition} in {city.title()}"
        trace.append(f"WeatherTool: Fetched data -> {result}")
        return "WeatherTool", result
    return None

def tool_text(q, trace):
    trace.append("TextProcessorTool: Fallback tool activated")
    
    if "upper" in q.lower():
        trace.append("TextProcessorTool: Logic 'UPPERCASE' selected based on keyword")
        return "TextProcessorTool", q.upper()
    elif "lower" in q.upper():
        trace.append("TextProcessorTool: Logic 'LOWERCASE' selected based on keyword")
        return "TextProcessorTool", q.lower()
    else:
        trace.append("TextProcessorTool: Logic 'Total Length of Prompt' selected")
        return "TextProcessorTool", str(len(q))


def run_agent(task):
    trace = [f"Agent: Received task '{task}'"]
    
    selected_tool = None
    final_output = None

    tools = [tool_calc, tool_weather, tool_text]

    for tool_func in tools:
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


class Request(BaseModel): task: str

@app.post("/process")
def process(req: Request):
    response = run_agent(req.task)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)