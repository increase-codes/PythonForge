
"""Demonstrate PythonForge with a simple transaction-processing workflow."""

from pythonforge.task import Task
from pythonforge.workflow import Workflow


def load_transactions() -> list[float]:
    """Return sample transaction amounts."""
    return [120.50, 80.00, 45.25]


def validate_transactions(amounts: list[float]) -> list[float]:
    """Reject negative transaction amounts and return valid data."""
    if any(amount < 0 for amount in amounts):
        raise ValueError("Transaction amounts cannot be negative.")

    return amounts


def calculate_total(amounts: list[float]) -> float:
    """Calculate the sum of all transaction amounts."""
    return sum(amounts)


def main() -> None:
    """Build and run the example workflow."""
    workflow = Workflow()

    # Register the data-loading task; it has no dependencies.
    workflow.add_task(
        Task("load", load_transactions)
    )

    # Validation consumes the list produced by the loading task.
    workflow.add_task(
        Task(
            "validate",
            validate_transactions,
            dependencies=["load"],
        )
    )

    # Calculation consumes the validated list.
    workflow.add_task(
        Task(
            "total",
            calculate_total,
            dependencies=["validate"],
        )
    )

    # Execute the workflow and retrieve results in registration order.
    results = workflow.run()

    print("PythonForge workflow completed successfully.")
    print(f"Loaded transactions: {results[0]}")
    print(f"Validated transactions: {results[1]}")
    print(f"Total transaction value: {results[2]:.2f}")


if __name__ == "__main__":
    main()
