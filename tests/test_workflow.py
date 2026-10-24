
"""Tests for PythonForge workflow execution."""

import pytest

from pythonforge.task import Task
from pythonforge.workflow import Workflow


# Verify that tasks execute in registration order.
def test_workflow_runs_tasks_in_order():
    # Create a workflow to coordinate the tasks.
    workflow = Workflow()

    # Register two tasks that return different values.
    workflow.add_task(Task("first", lambda: 10))
    workflow.add_task(Task("second", lambda: 20))

    # Verify that results preserve the tasks' registration order.
    assert workflow.run() == [10, 20]


# Verify that a task receives the result of its dependency.
def test_workflow_passes_dependency_result_to_next_task():
    # Create a workflow to coordinate the tasks.
    workflow = Workflow()

    # Register a task that produces a list of numbers.
    workflow.add_task(Task("load", lambda: [10, 20, 30]))

    # Register a task that consumes the result produced by "load".
    workflow.add_task(
        Task(
            "calculate_total",
            lambda numbers: sum(numbers),
            dependencies=["load"],
        )
    )

    # Verify that both task results are returned in registration order.
    assert workflow.run() == [[10, 20, 30], 60]


# Verify that execution fails when a dependency has no available result.
def test_workflow_rejects_missing_dependency():
    # Create a workflow to coordinate the task.
    workflow = Workflow()

    # Register a task that depends on a name that has no registered producer.
    workflow.add_task(
        Task(
            "calculate_total",
            lambda numbers: sum(numbers),
            dependencies=["missing_task"],
        )
    )

    # Verify that execution reports the unavailable dependency.
    with pytest.raises(ValueError, match="unknown task"):
        workflow.run()

        # Verify that circular dependencies are detected instead of running forever.
        def test_workflow_rejects_circular_dependencies():
            # Neither task can run because each depends on the other.
            workflow = Workflow()
            workflow.add_task(
                Task("task_a", lambda value: value, dependencies=["task_b"])
            )
            workflow.add_task(
                Task("task_b", lambda value: value, dependencies=["task_a"])
            )

            # The workflow should report the cycle clearly.
            with pytest.raises(ValueError, match="Circular dependency detected"):
                workflow.run()

        # Verify that task failures propagate through the workflow.
        def test_workflow_propagates_task_failure():
            # Register a task that deliberately raises an exception.
            workflow = Workflow()
            workflow.add_task(Task("failing_task", lambda: 1 / 0))

            # The original exception should reach the caller.
            with pytest.raises(ZeroDivisionError):
                workflow.run()


# Verify that circular dependencies are detected instead of running forever.
def test_workflow_rejects_circular_dependencies():
    workflow = Workflow()
    workflow.add_task(
        Task("task_a", lambda value: value, dependencies=["task_b"])
    )
    workflow.add_task(
        Task("task_b", lambda value: value, dependencies=["task_a"])
    )

    with pytest.raises(ValueError, match="Circular dependency detected"):
        workflow.run()


# Verify that task failures propagate through the workflow.
def test_workflow_propagates_task_failure():
    workflow = Workflow()
    workflow.add_task(Task("failing_task", lambda: 1 / 0))

    with pytest.raises(ZeroDivisionError):
        workflow.run()



# Verify that a task failure prevents dependent tasks from executing.
def test_workflow_stops_when_dependency_fails():
    workflow = Workflow()
    workflow.add_task(
        Task(
            "validate",
            lambda amounts: (
                (_ for _ in ()).throw(ValueError("Negative amount"))
                if any(amount < 0 for amount in amounts)
                else amounts
            ),
            dependencies=["load"],
        )
    )
    workflow.add_task(Task("load", lambda: [10, -5]))
    workflow.add_task(
        Task("total", lambda amounts: sum(amounts), dependencies=["validate"])
    )

    with pytest.raises(ValueError, match="Negative amount"):
        workflow.run()
