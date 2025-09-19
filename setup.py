from setuptools import setup

setup(
    name="mini-todo",
    version="1.0.0",
    py_modules=["mini_todo"],   # must match filename without .py
    entry_points={
        "console_scripts": [
            "todo = mini_todo:main",  # must match module name
        ],
    },
    install_requires=[],
    author="Your Name",
    description="A minimalist terminal-based to-do list CLI",
    url="https://github.com/sageauswest/mini-todo",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
