import pytest

from pythonforge import Task


def test_task_returns_function_result():
    task = Task("addition", lambda: 3 + 4)

    assert task.run() == 7


def test_task_propagates_function_error():
    task = Task("failure", lambda: 1 / 0)

    with pytest.raises(ZeroDivisionError):
        task.run()

def test_task_rejects_empty_name():
        with pytest.raises(ValueError):
            Task("   ", lambda: 42)

def test_task_rejects_non_callable_function():
        with pytest.raises(TypeError):
            Task("invalid", 42)





def test_task_rejects_non_string_name():
    with pytest.raises(ValueError, match="non-empty string"):
        Task(None, lambda: 42)


def test_task_rejects_non_list_dependencies():
    with pytest.raises(TypeError, match="list of strings"):
        Task("process", lambda: 42, dependencies="load")


def test_task_rejects_empty_dependency_name():
    with pytest.raises(ValueError, match="non-empty string"):
        Task("process", lambda: 42, dependencies=[" "])


def test_task_rejects_duplicate_dependencies():
    with pytest.raises(ValueError, match="duplicates"):
        Task("process", lambda value: value, dependencies=["load", "load"])


def test_task_copies_dependency_list():
    dependencies = ["load"]
    task = Task("process", lambda value: value, dependencies=dependencies)

    dependencies.append("validate")

    assert task.dependencies == ["load"]
