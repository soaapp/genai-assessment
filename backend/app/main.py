import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .agent import run_agent
from .db import init_db, log_request, fetch_history

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
    )

init_db()

class Request(BaseModel): 
    task: str

@app.post("/process")
def process(req: Request):
    response = run_agent(req.task)
    log_request(response)
    return response

@app.get("/history")
def get_history():
    return fetch_history()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)