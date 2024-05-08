import sqlite3
from pathlib import Path
from src.config import DB_PATH


class DBHandler:
    """A class to handle the SQLite database."""

    def __init__(self):
        self.conn = None

    def connect(self, db_path: Path = DB_PATH):
        try:
            self.conn = sqlite3.connect(db_path)
            self.create_table(self.conn)
        except sqlite3.Error as e:
            print(e)

        return self.conn

    def create_table(self, conn: sqlite3.Connection):
        """Create the table to store completed tasks."""
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS completed_tasks(id INTEGER PRIMARY KEY, tag TEXT, date_started TEXT, duration FLOAT)"
        )

    def log_task(self, task):
        """Log a completed task."""
        self.connect(DB_PATH)
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO completed_tasks VALUES(?, ?, ?, ?)",
            (None, task.tag.name, task.start_time, task.duration),
        )
        self.conn.commit()

    def fetch_tasks(self, n: int = 5):
        """Fetch all completed tasks."""
        self.connect(DB_PATH)
        cur = self.conn.cursor()
        cur.execute("")
        rows = cur.fetchall()
        return rows

    def clear_table(self):
        """Clear the table."""
        self.connect(DB_PATH)
        cur = self.conn.cursor()
        cur.execute("DELETE FROM completed_tasks")
        self.conn.commit()

    def __del__(self):
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    db_handler = DBHandler()

    db_handler.connect(DB_PATH)

    if db_handler.conn:
        # db_handler.clear_table()

        cur = db_handler.conn.cursor()
        cur.execute("SELECT * FROM completed_tasks")
        rows = cur.fetchall()
        if rows:
            print("Completed tasks:")
            for row in rows:
                print(row)
