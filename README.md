# PythonForge

PythonForge is a lightweight Python workflow engine for defining and executing tasks with dependencies.

It demonstrates core software engineering practices including object-oriented design, input validation, dependency-aware execution, failure handling, logging, automated testing, and Python package distribution.

## Features

- Define reusable tasks as Python callables.
- Declare dependencies between tasks.
- Execute tasks in dependency order and pass prerequisite results to dependent tasks.
- Detect invalid dependencies and circular dependency chains.
- Propagate task failures and log workflow execution.
- Expose a read-only tuple view of registered tasks.
- Run the demo through a command-line entry point, Python module, or root script.

## Requirements

- Python 3.13 or later
- pip

## Setup

Clone the repository and enter the project directory:

```powershell
git clone https://github.com/increase-codes/PythonForge.git
cd PythonForge
```

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project in editable mode and install the test runner:

```powershell
python -m pip install -e .
python -m pip install pytest
```

## Run the demo

```powershell
python -m pythonforge
```

Alternative entry points:

```powershell
pythonforge
python main.py
```

The demo processes sample transactions and calculates their total value, **245.75**.

## Run tests

```powershell
python -m pytest -v
```

The test suite covers task behavior, dependency handling, validation, failure cases, and workflow execution.

## Project structure

```text
PythonForge/
├── src/
│   └── pythonforge/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── demo.py
│       ├── task.py
│       └── workflow.py
├── tests/
│   ├── test_task.py
│   └── test_workflow.py
├── main.py
├── pyproject.toml
└── README.md
```

## Design overview

- **Task:** represents a unit of work and its dependencies.
- **Workflow:** registers tasks, validates dependencies, determines execution order, and manages results.
- **CLI and demo:** provide runnable examples of the engine.
- **Tests:** verify expected behavior and important failure conditions.

## Learning objectives

PythonForge is also a practical study of Python objects, functions, type hints, encapsulation, dependency resolution, exception handling, logging, testing, and packaging.

## Status

The current development baseline has 21 passing tests. This is a learning and portfolio project, not a claim of production readiness for arbitrary workloads.