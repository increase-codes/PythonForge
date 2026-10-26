
"""Test workflow registration, dependency resolution, and failure handling."""

import logging

import pytest

from pythonforge.task import Task
from pythonforge.workflow import Workflow


def test_workflow_runs_tasks_in_order():
    """Execute independent tasks in their registration order."""
    workflow = Workflow()
    workflow.add_task(Task("first", lambda: "first"))
    workflow.add_task(Task("second", lambda: "second"))

    assert workflow.run() == ["first", "second"]


def test_workflow_passes_dependency_result_to_next_task():
    """Pass a prerequisite's result into its dependent task."""
    workflow = Workflow()
    workflow.add_task(Task("load", lambda: 10))
    workflow.add_task(
        Task("double", lambda value: value * 2, dependencies=["load"])
    )

    assert workflow.run() == [10, 20]


def test_workflow_rejects_missing_dependency():
    """Reject dependencies that refer to unregistered tasks."""
    workflow = Workflow()
    workflow.add_task(
        Task("process", lambda value: value, dependencies=["missing"])
    )

    with pytest.raises(ValueError, match="unknown task"):
        workflow.run()


def test_workflow_rejects_circular_dependencies():
    """Reject dependency cycles that prevent execution."""
    workflow = Workflow()
    workflow.add_task(
        Task("first", lambda value: value, dependencies=["second"])
    )
    workflow.add_task(
        Task("second", lambda value: value, dependencies=["first"])
    )

    with pytest.raises(ValueError, match="Circular dependency detected"):
        workflow.run()


def test_workflow_rejects_self_dependency():
    """Reject a task that depends on its own result."""
    workflow = Workflow()
    workflow.add_task(
        Task("loop", lambda value: value, dependencies=["loop"])
    )

    with pytest.raises(ValueError, match="Circular dependency detected"):
        workflow.run()


def test_workflow_propagates_task_failure():
    """Let the original task exception reach the caller."""
    workflow = Workflow()
    workflow.add_task(Task("failure", lambda: 1 / 0))

    with pytest.raises(ZeroDivisionError):
        workflow.run()


def test_workflow_stops_when_dependency_fails():
    """Prevent downstream tasks from running after a prerequisite fails."""
    workflow = Workflow()
    executed = []

    def fail():
        """Simulate a prerequisite that fails during execution."""
        raise RuntimeError("task failed")

    def downstream(value):
        """Record execution so the test can verify whether it ran."""
        executed.append(value)
        return value

    workflow.add_task(Task("failure", fail))
    workflow.add_task(
        Task("downstream", downstream, dependencies=["failure"])
    )

    with pytest.raises(RuntimeError, match="task failed"):
        workflow.run()

    assert executed == []


def test_workflow_logs_successful_execution(caplog):
    """Verify that workflow start and completion are logged."""
    workflow = Workflow()

    with caplog.at_level(logging.INFO, logger="pythonforge.workflow"):
        workflow.run()

    assert "Starting workflow with 0 task(s)." in caplog.text
    assert "Workflow completed successfully." in caplog.text


def test_workflow_logs_task_failure(caplog):
    """Verify that failures are logged and exceptions still propagate."""
    workflow = Workflow()
    workflow.add_task(Task("broken_task", lambda: 1 / 0))

    with caplog.at_level(logging.ERROR, logger="pythonforge.workflow"):
        with pytest.raises(ZeroDivisionError):
            workflow.run()

    assert "Task 'broken_task' failed." in caplog.text




def test_workflow_rejects_non_task_objects():
    """Prevent objects without the Task contract from being registered."""
    workflow = Workflow()

    with pytest.raises(TypeError, match="only accepts Task instances"):
        workflow.add_task("not a task")


def test_workflow_rejects_duplicate_task_names():
    """Keep task names unique so dependency references remain unambiguous."""
    workflow = Workflow()
    workflow.add_task(Task("load", lambda: 10))

    with pytest.raises(ValueError, match="Duplicate task name"):
        workflow.add_task(Task("load", lambda: 20))