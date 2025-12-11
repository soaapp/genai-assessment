# GenAI Agent Assessment

Hello! I am Jay Jahanzad, an AI/ML Engineer with a huge passion for building and learning. This is my submission for the GenAI Coding Challenge. Big big thank you for looking at this and the team at  <img height="25" alt="bmo-logo" src="https://github.com/user-attachments/assets/55fc699a-5306-43ec-a56a-6c77172e4ff0" />


The following is a full-stack system that demonstrates agent-based task routing and tool execution. The agent analyzes user input and selects the appropriate tool to handle the request, returning both the result and a detailed execution trace.

## Features

- Agent-based task routing with three specialized tools (No LLMs used.)
    - Calculator for arithmetic operations
    - Weather mock tool for city weather queries
    - Text processor for string manipulation
- Full execution trace logging
- SQLite persistence for task history
- React frontend with Mantine UI
- RESTful API built with FastAPI

## Architecture


### HLD

<img width="415" height="1105" alt="HLD_BMO_assessment_drawio" src="https://github.com/user-attachments/assets/75625fff-c4d9-4a08-843b-25262718cfd9" />


### Sequence Diagram

<img width="8912" height="12570" alt="jay_ssd_bmo_assessment" src="https://github.com/user-attachments/assets/a700ebf4-9f4d-4519-aad3-95618eadf653" />


### Class Diagram

<img width="9062" height="6360" alt="jay_classdiag_bmo_assessment" src="https://github.com/user-attachments/assets/a9a5aca0-abe6-4239-896f-5b916455a810" />


## Prerequisites

- Python 3.10+ (tested on 3.14)
- Node.js 18+ (tested on 24.10)
- npm 8+ (tested on 11.6)

## Installation

### Backend

```bash
cd backend
python3 -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Running the Application

### Backend

From the backend directory with virtual environment activated:

```bash
python -m app.main
```

The API runs on `http://localhost:3001`

### Frontend

From the frontend directory:

```bash
npm run dev
```

The UI runs on `http://localhost:5173`

## Running Tests

```bash
cd backend
pytest -v
```

Tests cover:
- Calculator arithmetic evaluation
- Weather location extraction and mock response
- Text processor (uppercase, lowercase, count)
- History endpoint
- API integration


## API Endpoints

### POST /process

Accepts a user task and returns the result with execution trace.

Request:
```json
{
  "task": "What is 5 + 10"
}
```

Response:
```json
{
  "task": "What is 5 + 10",
  "output": "15",
  "tool": "CalculatorTool",
  "steps": [
    "Agent: Received task 'What is 5 + 10'",
    "CalculatorTool: Detected math expression '5 + 10'",
    "CalculatorTool: Successfully evaluated '5 + 10' = 15",
    "Agent: Final Output -> '15'"
  ],
  "ts": "2025-12-10T21:30:45.123456"
}
```

### GET /history

Returns the last 20 task executions from the database.

## Tools

### CalculatorTool
Detects and evaluates basic arithmetic expressions.

Example: `"5 + 10"` returns `"15"`

### WeatherMockTool
Detects weather queries and returns mock data for the specified city.

Example: `"Weather in Toronto"` returns `"12°C, Sunny in Toronto"`

### TextProcessorTool
Handles text manipulation tasks (uppercase, lowercase, character count).

Examples:
- `"uppercase hello"` returns `"UPPERCASE HELLO"`
- `"lowercase WORLD"` returns `"lowercase world"`
- `"random text"` returns `"11"` (total character count)

## Project Structure

```
genai-assessment/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI endpoints
│   │   ├── agent.py         # Agent logic
│   │   ├── tools.py         # Tool implementations
│   │   └── db.py            # Database layer
│   ├── tests/
│   │   └── test_api.py      # Unit tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
└── README.md
```

## Design Decisions

**Tool Selection**: 
Tools are evaluated sequentially. The first tool that matches the input pattern is selected and executed. This keeps the agent logic simple and predictable.

**Agent Logic/Solution**: 
The "agent" uses regex and keyword detection instead of an actual LLM integration. This was intentional to keep the system lightweight and fast. Also, I wanted to follow the direction of the assignment. Ensuring that my main focus is on architecture, readability, and solutioning. Over complicating the application would be a poor use of time and would stray away from the goal.

**Tool Interface**: 
All tools follow the same function signature `(query, trace) -> tuple | None`, making it straightforward to add new tools.

**Database**: 
Out of the options for persistence listed, SQLite was chosen for its simplicity and simple setup. SQLite also had many other benefits that I found for the purpose of this project to align well. 

Using in-memory had several issues that I considered such as it not "truly" being persisted. If the application were to restart, history would be lost. 

A JSON file is an industry standard for data but in this case I'd have several problems such as the lack of performance when writing/reading the file. Also querying JSON is not an ideal task. 

SQLite won for these overall reasons. If I needed to scale it would be very simple to add entries. It persists effectively, it's very queryable in case I wanted to implement that, and it is build into python as well! 

**Frontend Port**: 
Vite assigns the frontend port dynamically. The backend is fixed on port 3001 to match CORS configuration.


## Known Limitations

- CalculatorTool uses `eval()` for expression evaluation. This works for the demo but isn't suitable for production due to security concerns.
- Limited error handling on malformed inputs.
- No authentication or rate limiting. (Bonus RBAC Task is not implemented due to the decision that it would reduce code readability and was not a valuable trade off for this demo.)
- Tool selection is first-match only. Ambiguous inputs may not route to the intended tool.
- Execution traces in the history view could be formatted better for readability.

## Time Spent

Approximately 8-9 hours total:
- Architecture and Solution Designing: 2 hours
- Backend development: 2 hours
- Frontend development: 2 hours
- Testing and debugging: 1 hour
- Documentation: 1 hours

## Future Improvements

Given more time, I would add:

1. Add PROD level error handling and input validation.
2. Implement "streaming" so the logs (and potentially the response) could improve UX and logging experience. Adding streaming for the purpose of this demo was not the target, and wanted to focus on clean architecture with reliable logging,
3. Improve history UI to display execution steps more clearly and more similar to the logs shown
4. Add tool confidence scoring for better routing on ambiguous inputs, also more logic around falling back on the appropriate tool.
5. Support multi-step reasoning by chaining tools
6. Add integration tests and increase test coverage to unhappy paths
7. I think it would be very cool to add even a "guardrail" system that can ask to "Clarify task request" if no tool was selected.

## Environment

Tested on macOS with Python 3.14.0, Node 24.10.0, and npm 11.6.0. Should work on Windows and Linux with compatible versions.

## Special Mention
To my cat Pluto for always supporting me while I code. <img height="95" alt="Screenshot 2025-12-10 at 10 37 21 PM" src="https://github.com/user-attachments/assets/efc89bfd-f54a-4f89-b1ff-5ee9296bd4cc" />


