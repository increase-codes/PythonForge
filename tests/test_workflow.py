
from pythonforge.task import Task
from pythonforge.workflow import Workflow


def test_workflow_runs_tasks_in_order():
    workflow = Workflow()
    workflow.add_task(Task("first", lambda: 10))
    workflow.add_task(Task("second", lambda: 20))

    assert workflow.run() == [10, 20]
