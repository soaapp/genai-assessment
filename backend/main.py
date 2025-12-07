import sqlite3, json, re, datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def tool_calc(q):
    if match := re.search(r'[\d\.\s\+\-\*\/]+', q): 
        try: return "Calculator", str(eval(match.group(0).strip()))
        except: pass
    return None

def tool_weather(q):
    if "weather" in q.lower():
        # Extract city after "in", "at", or "for"
        city = next((q.split(p)[1].strip() for p in ["in ", "at ", "for "] if p in q), "Unknown")
        return "Weather", f"18°C, Clear in {city.title()}"
    return None

def tool_text(q):
    # Fallback
    return "TextProcessor", q.upper() if "upper" in q.lower() else q[::-1]

# Agent Logic
def run_agent(task):
    log = [f"Step 1: Input '{task}'"]
    
    name, output = next((res for t in [tool_calc, tool_weather] if (res := t(task))), tool_text(task))
    
    log.extend([f"Step 2: Selected {name}", f"Step 3: Output '{output}'"])
    return {"task": task, "output": output, "tool": name, "steps": log, "ts": datetime.datetime.now().isoformat()}

# API Section

class Request(BaseModel): task: str

@app.post("/process")
def process(req: Request):
    response = run_agent(req.task)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)