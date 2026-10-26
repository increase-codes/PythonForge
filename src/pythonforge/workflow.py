
"""Coordinate task registration and dependency-aware execution."""

import logging
from typing import Any

from pythonforge.task import Task


# Allow applications to configure logging for this module.
logger = logging.getLogger(__name__)


class Workflow:
    """Register tasks and execute them when their dependencies are ready."""

    def __init__(self) -> None:
        # Preserve registration order for predictable execution and results.
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Register a valid task with a unique name."""
        # Only Task instances can be registered.
        if not isinstance(task, Task):
            raise TypeError("Workflow only accepts Task instances.")

        # Dependency references require unique task names.
        if any(existing.name == task.name for existing in self.tasks):
            raise ValueError(f"Duplicate task name: {task.name}")

        self.tasks.append(task)

    def run(self) -> list[Any]:
        """Execute tasks in dependency order and return results in registration order."""
        logger.info("Starting workflow with %d task(s).", len(self.tasks))

        # Build a lookup so each dependency can be checked by name.
        tasks_by_name = {task.name: task for task in self.tasks}

        # Reject dependencies that do not refer to registered tasks.
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

        # Store completed results for downstream tasks.
        results: dict[str, Any] = {}
        pending = {task.name: task for task in self.tasks}

        # Execute tasks whose prerequisites have all completed.
        while pending:
            ready = [
                task
                for task in self.tasks
                if task.name in pending
                and all(name in results for name in task.dependencies)
            ]

            # No ready tasks means the remaining tasks are blocked by a cycle.
            if not ready:
                raise ValueError(
                    "Circular dependency detected among tasks: "
                    f"{list(pending)}"
                )

            for task in ready:
                # Pass prerequisite results in their declared dependency order.
                inputs = [results[name] for name in task.dependencies]

                logger.debug("Running task '%s'.", task.name)

                try:
                    results[task.name] = task.run(*inputs)
                except Exception:
                    # Record the traceback without suppressing the original error.
                    logger.exception("Task '%s' failed.", task.name)
                    raise

                logger.debug("Task '%s' completed successfully.", task.name)
                del pending[task.name]

        # Return results in registration order, regardless of execution order.
        ordered_results = [results[task.name] for task in self.tasks]

        logger.info("Workflow completed successfully.")

        return ordered_results
