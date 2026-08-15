# ✅ To-Do List (Tkinter GUI)
**Intern ID:** CITS8111

A simple desktop To-Do List app built with Python's built-in **Tkinter**
GUI toolkit. Supports full CRUD — create, read, update, and delete tasks —
with tasks saved locally so your list persists between runs.

No external dependencies required — just the Python standard library.

## Features

- ➕ **Create** — add new tasks via a text box (press Enter or click "Add Task")
- 📋 **Read** — view all tasks in a scrollable list; completed tasks are shown greyed out
- ✏️ **Update** — edit a task's title, or double-click / use "Toggle Done" to mark complete
- 🗑️ **Delete** — remove a single task, or clear all completed tasks at once
- 💾 **Persistence** — tasks are automatically saved to `tasks.json` and reloaded on startup

## Screenshot

```
┌─────────────────────────────────────────┐
│ [ Buy groceries               ] [Add Task]│
├─────────────────────────────────────────┤
│ [ ] Buy groceries                        │
│ [x] Finish report          (greyed out)  │
│ [ ] Call the dentist                     │
│                                           │
├─────────────────────────────────────────┤
│ [Toggle Done] [Edit] [Delete]  [Clear Completed] │
├─────────────────────────────────────────┤
│ 1/3 completed                            │
└─────────────────────────────────────────┘
```

## Requirements

- Python 3.8+
- Tkinter (included with most Python installations)

> **Note:** On some Linux distributions, Tkinter isn't installed by default.
> Install it with:
> ```bash
> sudo apt-get install python3-tk
> ```

## Installation & Usage

```bash
git clone https://github.com/<your-username>/todo-tkinter.git
cd todo-tkinter
python todo_app.py
```

That's it — no `pip install` needed, since Tkinter ships with Python.

## How to use

| Action | How |
|---|---|
| Add a task | Type in the box, press **Enter** or click **Add Task** |
| Mark done / not done | Select a task, click **Toggle Done**, or double-click it |
| Edit a task | Select a task, click **Edit**, update the text |
| Delete a task | Select a task, click **Delete**, confirm |
| Remove all completed | Click **Clear Completed** |

## Project structure

```
todo-tkinter/
├── todo_app.py              # Tkinter GUI (the app you run)
├── task_manager.py          # Core CRUD logic + JSON persistence (GUI-independent)
├── tests/
│   └── test_task_manager.py # Unit tests for CRUD logic
├── .github/workflows/ci.yml # CI: run tests on push/PR
├── .gitignore
├── LICENSE
└── README.md
```

The CRUD logic lives in `task_manager.py`, completely separate from the
GUI code in `todo_app.py`. This makes the core logic unit-testable
without needing a display — handy for CI environments.

## Running tests

```bash
pip install pytest
pytest tests/ -v
```

## Data storage

Tasks are stored in `tasks.json`, created automatically in the project
folder the first time you add a task. Delete this file to reset your list.

## Roadmap ideas

- [ ] Due dates and reminders
- [ ] Task priority levels / color coding
- [ ] Search / filter tasks
- [ ] Dark mode theme

## Contributing

Issues and pull requests are welcome. Please run `pytest` before submitting.

## License

MIT — see [LICENSE](LICENSE).
