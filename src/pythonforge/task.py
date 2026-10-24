
from collections.abc import Callable
from typing import Any


class Task:
    def __init__(
        self,
        name: str,
        function: Callable[..., Any],
        dependencies: list[str] | None = None,
    ) -> None:
        if not name.strip():
            raise ValueError("Task name cannot be empty.")

        if not callable(function):
            raise TypeError("Task function must be callable.")

        self.name = name
        self.function = function
        self.dependencies = dependencies or []

    def run(self, *args: Any) -> Any:
        return self.function(*args)
