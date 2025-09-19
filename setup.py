from setuptools import setup

setup(
    name="mini-todo",
    version="1.0.0",
    py_modules=["mini-todo"],  # the name of your Python script without .py
    entry_points={
        "console_scripts": [
            "todo = mini-todo:main",  # 'todo' is the command users will run
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
