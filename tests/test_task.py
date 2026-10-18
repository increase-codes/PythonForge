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




