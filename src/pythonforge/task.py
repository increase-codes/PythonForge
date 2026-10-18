
from collections.abc import Callable
from typing import Any


class Task:
    def __init__(self, name: str, function: Callable[[], Any]) -> None:
        if not name.strip():
            raise ValueError("Task name cannot be empty.")

        if not callable(function):
            raise TypeError("Task function must be callable.")

        self.name = name
        self.function = function

    def run(self) -> Any:
        return self.function()
