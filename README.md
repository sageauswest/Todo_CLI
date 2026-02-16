# Minimalist CLI Todo List

A minimalist terminal-based to-do list CLI with persistent storage and optional deadlines.  
Manage tasks quickly from your terminal.

## Features

- Add tasks with optional deadlines
- Toggle tasks as done or undone
- Edit task text and deadlines
- Delete tasks
- Human-friendly deadlines: Today, Tomorrow, This week, Next week

## Installation

### From GitHub

```bash
git clone https://github.com/sageauswest/mini-todo.git
cd mini-todo
pip install .
```

### MacOS (Homebrew Python) note

macOS users with Homebrew Python may get an "externally-managed-environment" error with pip.
Use pipx instead:

```bash
brew install pipx
pipx ensurepath
pipx install .
```
