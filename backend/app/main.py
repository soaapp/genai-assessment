"""FastAPI backend for the agent system"""

import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .agent import run_agent
from .db import init_db, log_request, fetch_history

app = FastAPI()

# Enable CORS for frontend communication (Set to * for ease of use during demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
    )

# Initialize database on startup
init_db()

class Request(BaseModel):
    task: str

@app.post("/process")
def process(req: Request):
    """Process a user task/request through the agent and log the interaction."""
    response = run_agent(req.task)
    log_request(response)
    return response

@app.get("/history")
def get_history():
    """Retrieve interaction history from the database."""
    return fetch_history()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)