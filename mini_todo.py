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

def format_task(task, idx):
    status = "[✔]" if task["done"] else "[ ]"
    lines = [f"{status} {idx}. {task['task']}"]
    if task.get("deadline"):
        lines.append(f"     Deadline: {task['deadline']}")
    return "\n".join(lines)

def main(stdscr):
    curses.curs_set(1)
    tasks = load_tasks()
    instructions = [
        "Minimalist To-Do List",
        "Commands:",
        "  add [task] [YYYY-MM-DD]",
        "  done [index]",
        "  undone [index]",
        "  edit [index] [new task]",
        "  delete [index]",
        "  deadline [index] [YYYY-MM-DD]",
        "  exit"
    ]

    user_input = ""
    status_message = ""

    while True:
        stdscr.clear()
        # Print instructions
        for i, line in enumerate(instructions):
            stdscr.addstr(i, 0, line)

        stdscr.addstr(len(instructions)+1, 0, "-"*50)

        # Display tasks (with multi-line support)
        if tasks:
            line_num = len(instructions) + 2
            for i, task in enumerate(tasks, start=1):
                for line in format_task(task, i).split("\n"):
                    stdscr.addstr(line_num, 0, line)
                    line_num += 1
                line_num += 1  # spacing between tasks
        else:
            stdscr.addstr(len(instructions)+3, 0, "Your to-do list is empty.")

        # Status / input
        height, width = stdscr.getmaxyx()
        stdscr.addstr(height-3, 0, "-"*width)
        stdscr.addstr(height-2, 0, "Status: " + status_message)
        stdscr.addstr(height-1, 0, "> " + user_input)
        stdscr.refresh()

        key = stdscr.getch()
        if key in (curses.KEY_BACKSPACE, 127, 8):
            user_input = user_input[:-1]
        elif key == ord('\n'):
            command = user_input.strip()
            status_message = ""
            if command.lower().startswith("add "):
                parts = command[4:].rsplit(" ", 1)
                task_text = parts[0].strip()
                deadline = parts[1] if len(parts) > 1 else ""
                created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                tasks.append({
                    "task": task_text,
                    "created_at": created_at,
                    "done": False,
                    "deadline": deadline
                })
                save_tasks(tasks)
                status_message = "Task added."
            elif command.lower().startswith("done "):
                try:
                    index = int(command[5:].strip()) - 1
                    tasks[index]["done"] = True
                    save_tasks(tasks)
                    status_message = "Marked done."
                except:
                    status_message = "Error: Invalid index."
            elif command.lower().startswith("undone "):
                try:
                    index = int(command[7:].strip()) - 1
                    tasks[index]["done"] = False
                    save_tasks(tasks)
                    status_message = "Marked undone."
                except:
                    status_message = "Error: Invalid index."
            elif command.lower().startswith("edit "):
                try:
                    parts = command[5:].strip().split(" ", 1)
                    index = int(parts[0]) - 1
                    new_task = parts[1].strip()
                    tasks[index]["task"] = new_task
                    save_tasks(tasks)
                    status_message = "Task updated."
                except:
                    status_message = "Error: Usage edit [index] [new task]"
            elif command.lower().startswith("delete "):
                try:
                    index = int(command[7:].strip()) - 1
                    tasks.pop(index)
                    save_tasks(tasks)
                    status_message = "Task deleted."
                except:
                    status_message = "Error: Invalid index."
            elif command.lower().startswith("deadline "):
                try:
                    parts = command[9:].strip().split(" ", 1)
                    index = int(parts[0]) - 1
                    tasks[index]["deadline"] = parts[1].strip()
                    save_tasks(tasks)
                    status_message = "Deadline updated."
                except:
                    status_message = "Error: Usage deadline [index] [YYYY-MM-DD]"
            elif command.lower() == "exit":
                break
            else:
                status_message = "Invalid command."
            user_input = ""
        else:
            try:
                user_input += chr(key)
            except:
                pass

# Launcher function for console_scripts
def cli():
    curses.wrapper(main)
