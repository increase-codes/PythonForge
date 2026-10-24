
"""Coordinate task registration and dependency-aware execution."""

from typing import Any

from pythonforge.task import Task


class Workflow:
    """Register tasks and execute them when their dependencies are ready."""

    def __init__(self) -> None:
        # Keep registration order for predictable execution and result output.
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Register a valid task with a unique name."""
        # Reject objects that do not follow the Task interface.
        if not isinstance(task, Task):
            raise TypeError("Workflow only accepts Task instances.")

        # Names identify tasks and connect dependencies to their producers.
        if any(existing.name == task.name for existing in self.tasks):
            raise ValueError(f"Duplicate task name: {task.name}")

        self.tasks.append(task)

    def run(self) -> list[Any]:
        """Execute tasks in dependency order and return results in registration order."""
        # Index tasks by name so dependency references can be checked quickly.
        tasks_by_name = {task.name: task for task in self.tasks}

        # Detect references to tasks that were never registered.
        for task in self.tasks:
            missing = [
                name
                for name in task.dependencies
                if name not in tasks_by_name
            ]

            if missing:
                raise ValueError(
                    f"Task '{task.name}' depends on unknown task(s): {missing}"
                )

        # Store completed results so dependent tasks can consume them.
        results: dict[str, Any] = {}

        # Initially, every registered task is waiting to execute.
        pending = {task.name: task for task in self.tasks}

        # Continue until every task has completed or a dependency cycle is found.
        while pending:
            # A task is ready only when all its dependencies have results.
            ready = [
                task
                for task in self.tasks
                if task.name in pending
                and all(name in results for name in task.dependencies)
            ]

            # If nothing can run, the remaining tasks depend on one another.
            if not ready:
                raise ValueError(
                    "Circular dependency detected among tasks: "
                    f"{list(pending)}"
                )

            # Run the currently ready tasks and save each result by task name.
            for task in ready:
                inputs = [results[name] for name in task.dependencies]
                results[task.name] = task.run(*inputs)
                del pending[task.name]

        # Preserve the original output contract, regardless of execution order.
        return [results[task.name] for task in self.tasks]
