"""Command line interface for the task tracker."""

from typing import Annotated
import typer

from src.config import DEFAULT_TAGS
from src.utils import TaskHandler
from src.database import DBHandler

app = typer.Typer()
db = DBHandler()
handler = TaskHandler(db)


@app.command()
def start(tag: Annotated[str, typer.Argument(help="The tag for the task.")]):
    """Start a new task."""
    if tag.upper() not in DEFAULT_TAGS:
        typer.confirm(
            f"Unknown tag {tag.upper()}. Valid task tags are {DEFAULT_TAGS}.\nDo you want to create a new task using the tag 'OTHER'?",
            abort=True,
        )
        tag = "OTHER"

    handler.start(tag)


@app.command()
def pause():
    """Pause current task."""
    handler.pause()


@app.command()
def resume():
    """Resume paused task."""
    handler.resume()


@app.command()
def finish():
    """Mark current task as completed."""
    handler.finish()


@app.command()
def abort():
    """Abandon current task."""
    handler.abort()


@app.command()
def reset():
    """Reset the current task."""
    handler.reset()


@app.command()
def status():
    """Show what task is being worked on and its status."""
    handler.show_status()


@app.command()
def report():
    """Show a report of all tasks."""
    handler.show_overview()


@app.command()
def show(n: Annotated[int, typer.Argument(help="Number of tasks to show.")] = 5):
    """Show the last n tasks."""
    handler.show_tasks(n)


@app.command()
def clear():
    """Clear all tasks from the database."""
    if typer.confirm("Do you want to clear the database?"):
        db.clear_table()
        print("Database cleared.")


if __name__ == "__main__":
    app()
