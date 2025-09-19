from setuptools import setup

setup(
    name="mini-todo",
    version="1.0.0",
    py_modules=["mini_todo"],          # matches the filename
    entry_points={
        "console_scripts": [
            "todo = mini_todo:cli",   # points to the wrapper function
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
