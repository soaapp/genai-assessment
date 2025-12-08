import sqlite3, json, re, datetime, random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


# Persistence Layer (Utilizing SQLite)
DB_NAME = "agent_history.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS interactions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            timestamp TEXT,
                            task TEXT,
                            tool_used TEXT,
                            final_output TEXT,
                            steps_log TEXT
                       )
                ''')
        conn.commit()

def log_request(data):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                INSERT INTO interactions (timestamp, task, tool_used, final_output, steps_log)
                VALUES (?, ?, ?, ?, ?)
                       ''', (
                           data["ts"],
                           data["task"],
                           data["tool"],
                           str(data["output"]),
                           json.dumps(data["steps"])
                       ))
        conn.commit()
        print(f"Saved task request '{data['task']}' to SQLite database.")


init_db()

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
        
        # TODO: If the city is still Unknown maybe we can fallback on saying "Unable to get weather"
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
    elif "lower" in q.lower():
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
    log_request(response)
    return response

@app.get("/history")
def get_history():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM interactions ORDER BY id DESC LIMIT 20")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)