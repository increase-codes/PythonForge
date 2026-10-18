
from typing import Any

from pythonforge.task import Task


class Workflow:
    def __init__(self) -> None:
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        if not isinstance(task, Task):
            raise TypeError("Workflow only accepts Task instances.")

        self.tasks.append(task)

    def run(self) -> list[Any]:
        results = []

        for task in self.tasks:
            results.append(task.run())

        return results
