# Task Tracker
*Developed by: [Mavromatis, Nikolaos](mailto:nck.mavromatis@gmail.com)*

A CLI application to easily track tasks you're working on.

## Quick Setup
In a terminal, navigate to the directory where you want to clone this repository.
```bash
cd path/to/folder
```

Clone this repository.
```bash
git clone https://github.com/nikolaos-mavromatis/task-tracker.git
```

Move into the newly created directory, create a virtual environment and install required packages.
```bash
cd task-tracker
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

You can start issuing commands to the task tracker. For example, to start a coding task:
```bash
python3 cli.py start coding
```

![alt text](assets/start-task.png)

For an overview of the available commands, run the following – see also image below.
```bash
python3 cli.py --help
```

![alt text](assets/app-help.png)

## Functional Requirements
> The **user** must be able to...
- [x] start a task with a specific tag.
- [x] pause/resume a task that is in progress.
- [x] mark a task as finished.
- [x] abort a task, i.e., abandon the task in progress.
- [x] view the status of the task tracker.
- [x] view last N number of tasks that were worked on.
- [ ] view a breakdown of the tasks worked on on a specific date.
- [x] reset timer of current task.
- [ ] switch through tasks seamlessly, i.e., not having to explicitly finish one task in order to start another.
- [ ] define new tags for tasks.

> The **app** must...
- [x] save completed tasks in a local database.
- [x] keep track of total time of active work spent on a single task. 
- [x] have a set of predefined tags for task types.
- [x] print useful messages when the user:
  - [x] tries to interact with a task when there is no task running.
  - [x] starts a task with a new tag.
  - [x] starts a task with the same tag as the current task.
  - [x] pauses the tracker when a task is already paused.
  - [x] resumes the tracker when there is no paused task.

