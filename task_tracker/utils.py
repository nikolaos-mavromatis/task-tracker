"""Utility functions for task management."""

import datetime
import json
import os
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from task_tracker.config import (
    CURRENT_TASK_FILE,
    DATETIME_FORMAT,
    DB_PATH,
    DEFAULT_TAGS,
    EMPTY_TASK,
    NO_TASK_MSG,
)


@dataclass
class Tag:
    """Dataclass for task tags."""

    name: str | None = field(default="NONE")
    valid_tags: list[str] = field(
        default_factory=lambda: DEFAULT_TAGS,
        init=False,
        repr=False,
        hash=False,
        compare=False,
    )

    def __post_init__(self):
        if not isinstance(self.name, str):
            raise TypeError(f"Tag name must be a string. Got {type(self.name)}.")

        self.name = self.name.upper()

        # `NONE` is a reserved tag for empty tasks
        if self.name not in [*DEFAULT_TAGS, "NONE"]:
            raise ValueError(
                f"Invalid tag {self.name}. Must be one of {self.valid_tags}."
            )

    def __str__(self) -> str:
        return self.name if self.name else "NONE"

    def __repr__(self) -> str:
        return self.name if self.name else "NONE"


class Task:
    """A class to represent a task."""

    def __init__(
        self,
        tag: str | None,
        start_time: str | None = None,
        last_resumed: str | None = None,
        duration: float = 0.0,
        status: str = "IN PROGRESS",
    ):
        self.tag = Tag(tag)
        self.start_time = (
            datetime.datetime.strptime(start_time, DATETIME_FORMAT)
            if start_time
            else datetime.datetime.now()
        )
        self.last_resumed = (
            datetime.datetime.strptime(last_resumed, DATETIME_FORMAT)
            if last_resumed
            else datetime.datetime.now()
        )
        self.duration = duration
        self.status = status

        self.formatted_start_time = (
            start_time
            if start_time
            else datetime.datetime.strftime(self.start_time, DATETIME_FORMAT)
        )

    def __str__(self):
        """Return a string representation of the task."""
        return (
            f"Task: {self.tag}\n"
            + (f"Started at: {self.formatted_start_time}\n" if self.start_time else "")
            + f"Status: {self.status}"
        )

    @classmethod
    def from_json(cls, filepath: Path):
        """Alternate constructor to create a Task object from a json file."""
        with open(filepath, "r", encoding="utf-8") as file:
            current_task = json.load(file)

        return cls(
            tag=current_task["tag"],
            start_time=current_task["start_time"],
            last_resumed=current_task["last_resumed"],
            duration=current_task["duration"],
            status=current_task["status"],
        )

    def to_json(self, filepath: Path):
        """Save the task object to a json file."""
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(
                {
                    "tag": self.tag.name,
                    "start_time": (
                        self.formatted_start_time if self.start_time else None
                    ),
                    "last_resumed": datetime.datetime.strftime(
                        self.last_resumed, DATETIME_FORMAT
                    ),
                    "duration": self.duration,
                    "status": self.status,
                },
                file,
            )

    @property
    def info(self) -> tuple[Tag | str | None, str, float]:
        """Return information about the task."""

        return (
            self.tag,
            datetime.datetime.strftime(self.start_time, DATETIME_FORMAT),
            self.duration,
        )


class TaskHandler:
    """A class to handle tasks."""

    def __init__(self, db):
        if not os.path.exists(CURRENT_TASK_FILE):
            os.makedirs(os.path.dirname(CURRENT_TASK_FILE), exist_ok=True)

            self._write_empty_task()

        self.task = Task.from_json(CURRENT_TASK_FILE)
        self.task_in_progress = self.task.tag.name != "NONE"
        self.db = db

    def start(self, tag: str):
        """Start a new task."""
        if self.task.tag.name == tag.upper() and self.task.status == "IN PROGRESS":
            print(f"Aleady working on {self.task.tag}.")
            return

        if self.task.tag.name == tag.upper() and self.task.status == "PAUSED":
            print(f"{self.task.tag} was paused. Resuming the task.")
            self.resume()
            return

        if self.task_in_progress:
            self.finish()

        self.task = Task(tag)
        self.task.to_json(CURRENT_TASK_FILE)

        print(self.task)

    def pause(self):
        """Pause the current task and save stint into the json file."""
        if self.task.status == "IN PROGRESS":
            self._update_task_duration()
            self.task.status = "PAUSED"

            self.task.to_json(CURRENT_TASK_FILE)

            print(f"Paused {self.task.tag}.")
            return

        if self.task.status == "PAUSED":
            print(f"{self.task.tag} is already paused.")
            return

        print(NO_TASK_MSG)

    def resume(self):
        """Resume the paused task."""
        if self.task.status == "IN PROGRESS":
            print(f"{self.task.tag} is already in progress.")
            return

        if self.task.status == "PAUSED":
            self.task.last_resumed = datetime.datetime.now()
            self.task.status = "IN PROGRESS"

            self.task.to_json(CURRENT_TASK_FILE)

            print(self.task)
            return

        print(NO_TASK_MSG)

    def abort(self):
        """Abort the current task."""
        if self.task_in_progress:
            self._write_empty_task()
            print(f"Aborted {self.task.tag}.")

            return

        print(NO_TASK_MSG)

    def finish(self):
        """Mark the task as finished."""
        if self.task_in_progress:
            self._update_task_duration()
            self.task.status = "FINISHED"

            print(
                f"Finished {self.task.tag}. Duration: {self.task.duration:.0f} seconds."
            )

            self.db.log_task(self.task)

            self._write_empty_task()

            return

        print(NO_TASK_MSG)

    def reset(self):
        """Reset current task, i.e., start a new task using the current task's tag."""
        if self.task_in_progress:
            self.task = Task(self.task.tag.name)

            self.task.to_json(CURRENT_TASK_FILE)
            print(f"Reset {self.task.tag} duration.")

            return

        print(NO_TASK_MSG)

    def show_tasks(self, n: int = 5):
        """View the last n tasks."""
        self.db.connect(DB_PATH)
        tasks = pd.read_sql_query(
            f"SELECT * FROM completed_tasks ORDER BY date_started DESC LIMIT {n}",
            self.db.conn,
        )

        print(tasks)

    def show_status(self):
        """Show the status of the current task."""
        if not self.task_in_progress:
            print(NO_TASK_MSG)
            return

        if self.task.status == "PAUSED":
            self.task.start_time = None

        print(self.task)

    def show_overview(self):
        """Show the overview of the tasks."""
        self.db.connect(DB_PATH)
        tasks = (
            pd.read_sql_query("select * from completed_tasks", self.db.conn)
            .assign(date_started=lambda x: pd.to_datetime(x["date_started"]).dt.date)
            .groupby(["date_started", "tag"])
            .agg({"duration": "sum"})
            .sort_values(["date_started", "duration"], ascending=[True, False])
        )

        print(tasks)

    def _write_empty_task(self):
        """Replace current task with an empty task."""
        with open(CURRENT_TASK_FILE, "w", encoding="utf-8") as file:
            json.dump(EMPTY_TASK, file)

    def _update_task_duration(self):
        """Set the duration of the task."""
        self.task.duration += (
            datetime.datetime.now() - self.task.last_resumed
        ).total_seconds()


if __name__ == "__main__":
    ...
