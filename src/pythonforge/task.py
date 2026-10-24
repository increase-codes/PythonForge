
"""Define a validated unit of work for a PythonForge workflow."""

from collections.abc import Callable
from typing import Any


class Task:
    """Represent a named function and the tasks that must precede it."""

    def __init__(
        self,
        name: str,
        function: Callable[..., Any],
        dependencies: list[str] | None = None,
    ) -> None:
        """Validate task configuration and store an independent configuration."""
        # A task name must be a non-empty string used for dependency lookup.
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Task name must be a non-empty string.")

        # Only callable objects can be executed as task functions.
        if not callable(function):
            raise TypeError("Task function must be callable.")

        # Dependencies must be a list of non-empty task-name strings.
        if dependencies is not None:
            if not isinstance(dependencies, list):
                raise TypeError("Task dependencies must be a list of strings.")

            if any(
                not isinstance(dependency, str) or not dependency.strip()
                for dependency in dependencies
            ):
                raise ValueError(
                    "Each dependency must be a non-empty string."
                )

            if len(dependencies) != len(set(dependencies)):
                raise ValueError("Task dependencies must not contain duplicates.")

        self.name = name
        self.function = function

        # Copy the list so later changes to the caller's list do not affect this task.
        self.dependencies = list(dependencies) if dependencies is not None else []

    def run(self, *args: Any) -> Any:
        """Execute the task function with results supplied by its dependencies."""
        return self.function(*args)
