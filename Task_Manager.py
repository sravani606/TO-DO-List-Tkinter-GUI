"""
task_manager.py
Core CRUD logic for the To-Do app, kept separate from the GUI so it
can be unit tested without a display.

Tasks are persisted to a local JSON file.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import List, Optional

DEFAULT_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")


@dataclass
class Task:
    id: int
    title: str
    done: bool = False


class TaskManager:
    """Handles create, read, update, delete, and persistence of tasks."""

    def __init__(self, data_file: str = DEFAULT_DATA_FILE):
        self.data_file = data_file
        self.tasks: List[Task] = []
        self._next_id = 1
        self.load()

    # ---------- CRUD ----------

    def add_task(self, title: str) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        task = Task(id=self._next_id, title=title, done=False)
        self.tasks.append(task)
        self._next_id += 1
        self.save()
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        return next((t for t in self.tasks if t.id == task_id), None)

    def list_tasks(self) -> List[Task]:
        return list(self.tasks)

    def update_task(self, task_id: int, title: Optional[str] = None,
                     done: Optional[bool] = None) -> Task:
        task = self.get_task(task_id)
        if task is None:
            raise KeyError(f"No task with id {task_id}")
        if title is not None:
            title = title.strip()
            if not title:
                raise ValueError("Task title cannot be empty.")
            task.title = title
        if done is not None:
            task.done = done
        self.save()
        return task

    def toggle_done(self, task_id: int) -> Task:
        task = self.get_task(task_id)
        if task is None:
            raise KeyError(f"No task with id {task_id}")
        task.done = not task.done
        self.save()
        return task

    def delete_task(self, task_id: int) -> None:
        task = self.get_task(task_id)
        if task is None:
            raise KeyError(f"No task with id {task_id}")
        self.tasks.remove(task)
        self.save()

    def clear_completed(self) -> int:
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if not t.done]
        self.save()
        return before - len(self.tasks)

    # ---------- Persistence ----------

    def save(self) -> None:
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump([asdict(t) for t in self.tasks], f, indent=2)

    def load(self) -> None:
        if not os.path.exists(self.data_file):
            self.tasks = []
            self._next_id = 1
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except (json.JSONDecodeError, OSError):
            self.tasks = []
            self._next_id = 1
            return

        self.tasks = [Task(**item) for item in raw]
        self._next_id = (max((t.id for t in self.tasks), default=0)) + 1
