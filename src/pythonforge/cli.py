
"""Command-line interface for PythonForge."""

import argparse
import logging
from pythonforge.demo import main as run_demo


def main() -> int:
    """Parse command-line arguments and execute the selected command."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    parser = argparse.ArgumentParser(
        prog="pythonforge",
        description="Run PythonForge workflow demonstrations.",
    )

    parser.add_argument(
        "command",
        nargs="?",
        choices=("demo",),
        default="demo",
        help="Workflow to run (default: demo).",
    )

    args = parser.parse_args()

    if args.command == "demo":
        run_demo()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
