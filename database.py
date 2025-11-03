conn = sqlite3.connect("tasks.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    due_date TEXT,
    done INTEGER DEFAULT 0
)
""")
conn.commit()