from enum import Enum
from pathlib import Path

ROOT = Path(__file__).parents[1]
"""The root directory of the project."""

EMPTY_TASK = {
    "tag": "NONE",
    "start_time": None,
    "last_resumed": None,
    "duration": 0.0,
    "status": None,
}
"""A dictionary representing an empty task."""

CURRENT_TASK_FILE = ROOT / "var" / "tmp" / ".current_task.json"
"""The file to store the current task."""

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
"""The format for datetime objects."""

DB_PATH = ROOT / "var" / "tasks.db"
"""The path to the SQLite database file."""

NO_TASK_MSG = "No task is currently running."
"""The message to display when no task is running."""

DEFAULT_TAGS = ["CODING", "MEETING", "TRAINING", "BREAK", "OTHER"]
"""The default tags for tasks."""
