#!/usr/bin/env python3
"""
todo_app.py
A simple To-Do List desktop app built with Tkinter.

Features (CRUD):
- Create: add new tasks
- Read:   view all tasks in a list, with completed tasks shown struck-through
- Update: edit a task's title, or toggle it done/not done
- Delete: remove a task, or clear all completed tasks

Run with:
    python todo_app.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from task_manager import TaskManager


class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("To-Do List")
        self.geometry("480x520")
        self.minsize(400, 400)

        self.manager = TaskManager()

        self._build_widgets()
        self._refresh_list()

    # ---------- UI construction ----------

    def _build_widgets(self):
        # Entry row for adding new tasks
        entry_frame = ttk.Frame(self, padding=10)
        entry_frame.pack(fill="x")

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(entry_frame, textvariable=self.entry_var)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.entry.bind("<Return>", lambda event: self._add_task())
        self.entry.focus()

        add_btn = ttk.Button(entry_frame, text="Add Task", command=self._add_task)
        add_btn.pack(side="left")

        # Task list
        list_frame = ttk.Frame(self, padding=(10, 0))
        list_frame.pack(fill="both", expand=True)

        self.listbox = tk.Listbox(
            list_frame, activestyle="none", selectmode="browse", font=("Segoe UI", 11)
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<Double-Button-1>", lambda event: self._toggle_done())

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Action buttons
        btn_frame = ttk.Frame(self, padding=10)
        btn_frame.pack(fill="x")

        ttk.Button(btn_frame, text="Toggle Done", command=self._toggle_done).pack(
            side="left", padx=(0, 6)
        )
        ttk.Button(btn_frame, text="Edit", command=self._edit_task).pack(
            side="left", padx=6
        )
        ttk.Button(btn_frame, text="Delete", command=self._delete_task).pack(
            side="left", padx=6
        )
        ttk.Button(btn_frame, text="Clear Completed", command=self._clear_completed).pack(
            side="right"
        )

        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self, textvariable=self.status_var, anchor="w", padding=(10, 4))
        status_bar.pack(fill="x")

    # ---------- Helpers ----------

    def _refresh_list(self):
        self.listbox.delete(0, "end")
        tasks = self.manager.list_tasks()
        for task in tasks:
            prefix = "[x]" if task.done else "[ ]"
            self.listbox.insert("end", f"{prefix} {task.title}")
            if task.done:
                self.listbox.itemconfig("end", fg="gray")

        total = len(tasks)
        done = sum(1 for t in tasks if t.done)
        self.status_var.set(f"{done}/{total} completed")

    def _selected_task(self):
        selection = self.listbox.curselection()
        if not selection:
            return None
        index = selection[0]
        tasks = self.manager.list_tasks()
        if index >= len(tasks):
            return None
        return tasks[index]

    # ---------- CRUD actions ----------

    def _add_task(self):
        title = self.entry_var.get()
        try:
            self.manager.add_task(title)
        except ValueError as exc:
            messagebox.showwarning("Invalid task", str(exc))
            return
        self.entry_var.set("")
        self._refresh_list()

    def _toggle_done(self):
        task = self._selected_task()
        if task is None:
            messagebox.showinfo("No selection", "Select a task first.")
            return
        self.manager.toggle_done(task.id)
        self._refresh_list()

    def _edit_task(self):
        task = self._selected_task()
        if task is None:
            messagebox.showinfo("No selection", "Select a task first.")
            return
        new_title = simpledialog.askstring(
            "Edit task", "Update task title:", initialvalue=task.title, parent=self
        )
        if new_title is None:
            return  # cancelled
        try:
            self.manager.update_task(task.id, title=new_title)
        except ValueError as exc:
            messagebox.showwarning("Invalid task", str(exc))
            return
        self._refresh_list()

    def _delete_task(self):
        task = self._selected_task()
        if task is None:
            messagebox.showinfo("No selection", "Select a task first.")
            return
        if messagebox.askyesno("Delete task", f"Delete '{task.title}'?"):
            self.manager.delete_task(task.id)
            self._refresh_list()

    def _clear_completed(self):
        removed = self.manager.clear_completed()
        self._refresh_list()
        if removed:
            self.status_var.set(f"Removed {removed} completed task(s)")


def main():
    app = TodoApp()
    app.mainloop()


if __name__ == "__main__":
    main()
