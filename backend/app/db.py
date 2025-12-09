import sqlite3, json

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


def fetch_history(limit = 20):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM interactions ORDER BY id DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        return {"error": str(e)}