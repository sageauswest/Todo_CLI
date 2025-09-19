#!/usr/bin/env python3
import curses
import datetime
import json
import os

DATA_FILE = os.path.expanduser("~/.todo_data.json")

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def human_deadline(deadline_str):
    if not deadline_str:
        return "No deadline"
    try:
        deadline_date = datetime.datetime.strptime(deadline_str, "%Y-%m-%d").date()
    except ValueError:
        return deadline_str
    today = datetime.date.today()
    delta = (deadline_date - today).days
    if delta == 0: return "Today"
    if delta == 1: return "Tomorrow"
    if 2 <= delta <= 7: return "This week"
    if 8 <= delta <= 14: return "Next week"
    return deadline_date.strftime("%Y-%m-%d")

def display_tasks(tasks):
    lines = []
    if not tasks:
        lines.append("Your to-do list is empty.\n")
        return lines
    for idx, task in enumerate(tasks, start=1):
        check = "✔" if task["done"] else " "
        lines.append(f"[{check}] {idx}. {task['task']}")
        lines.append(f"     Deadline: {human_deadline(task.get('deadline', ''))}\n")
    return lines

def main(stdscr):
    curses.curs_set(1)
    height, width = stdscr.getmaxyx()
    tasks = load_tasks()

    instructions = [
        "Minimalist To-Do List",
        "Commands:",
        "  add [task] [YYYY-MM-DD]",
        "  done [index]",
        "  undone [index]",
        "  edit [index] [new task text]",
        "  delete [index]",
        "  deadline [index] [YYYY-MM-DD]",
        "  exit"
    ]

    user_input = ""
    status_message = ""

    while True:
        stdscr.clear()
        for i, line in enumerate(instructions):
            stdscr.addstr(i, 0, line)

        task_lines = display_tasks(tasks)
        for i, line in enumerate(task_lines):
            stdscr.addstr(len(instructions)+1+i, 0, line)

        stdscr.addstr(height-3, 0, "-"*width)
        stdscr.addstr(height-2, 0, "Status: " + status_message)
        stdscr.addstr(height-1, 0, "> " + user_input)
        stdscr.refresh()

        key = stdscr.getch()
        if key in (curses.KEY_BACKSPACE, 127, 8):
            user_input = user_input[:-1]
        elif key == ord("\n"):
            command = user_input.strip()
            status_message = ""

            # ADD TASK (with optional deadline)
            if command.lower().startswith("add "):
                parts = command[4:].strip().rsplit(" ", 1)
                task_text = parts[0].strip()
                deadline = ""
                if len(parts) == 2:
                    maybe_date = parts[1].strip()
                    try:
                        datetime.datetime.strptime(maybe_date, "%Y-%m-%d")
                        deadline = maybe_date
                    except ValueError:
                        task_text = command[4:].strip()
                        deadline = ""
                if task_text:
                    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    tasks.append({
                        "task": task_text,
                        "created_at": created_at,
                        "done": False,
                        "deadline": deadline
                    })
                    save_tasks(tasks)
                    status_message = "Task added."
                else:
                    status_message = "Error: Task cannot be empty."

            # DONE / UNDONE
            elif command.lower().startswith("done ") or command.lower().startswith("undone "):
                try:
                    index = int(command.split()[1]) - 1
                    if 0 <= index < len(tasks):
                        if command.lower().startswith("done "):
                            tasks[index]["done"] = True
                        else:
                            tasks[index]["done"] = False
                        save_tasks(tasks)
                        status_message = "Task status updated."
                    else:
                        status_message = "Error: Invalid index."
                except (ValueError, IndexError):
                    status_message = "Error: Provide a valid index."

            # DELETE
            elif command.lower().startswith("delete "):
                try:
                    index = int(command[7:].strip()) - 1
                    if 0 <= index < len(tasks):
                        tasks.pop(index)
                        save_tasks(tasks)
                        status_message = "Task deleted."
                    else:
                        status_message = "Error: Invalid index."
                except ValueError:
                    status_message = "Error: Provide a valid index."

            # DEADLINE
            elif command.lower().startswith("deadline "):
                try:
                    parts = command[9:].strip().split(" ")
                    index = int(parts[0]) - 1
                    deadline = parts[1].strip()
                    datetime.datetime.strptime(deadline, "%Y-%m-%d")  # validate
                    if 0 <= index < len(tasks):
                        tasks[index]["deadline"] = deadline
                        save_tasks(tasks)
                        status_message = "Deadline updated."
                    else:
                        status_message = "Error: Invalid index."
                except (ValueError, IndexError):
                    status_message = "Error: Usage: deadline [index] [YYYY-MM-DD]"

            # EDIT TASK
            elif command.lower().startswith("edit "):
                try:
                    parts = command[5:].strip().split(" ", 1)
                    index = int(parts[0]) - 1
                    if 0 <= index < len(tasks):
                        new_text = parts[1] if len(parts) > 1 else ""
                        deadline = tasks[index]["deadline"]
                        # Check for optional /by
                        if "/by" in new_text:
                            text_parts = new_text.split("/by")
                            new_text = text_parts[0].strip()
                            maybe_date = text_parts[1].strip()
                            try:
                                datetime.datetime.strptime(maybe_date, "%Y-%m-%d")
                                deadline = maybe_date
                            except ValueError:
                                status_message = "Error: Invalid date format for /by."
                                user_input = ""
                                continue
                        if new_text:
                            tasks[index]["task"] = new_text
                        tasks[index]["deadline"] = deadline
                        save_tasks(tasks)
                        status_message = "Task edited."
                    else:
                        status_message = "Error: Invalid index."
                except (ValueError, IndexError):
                    status_message = "Error: Usage: edit [index] [new task text] (/by optional YYYY-MM-DD)"

            # EXIT
            elif command.lower() == "exit":
                break
            else:
                status_message = "Invalid command."

            user_input = ""
        else:
            try:
                user_input += chr(key)
            except ValueError:
                pass

if __name__ == "__main__":
    curses.wrapper(main)
