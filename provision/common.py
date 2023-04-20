# pylint: disable=redefined-builtin
from rich import print
from rich.panel import Panel


def print_success(msg):
    """Print success message."""
    return print(Panel(msg, style="green bold"))


def print_warn(msg):
    """Print warning message."""
    return print(Panel(msg, style="yellow bold"))


def print_error(msg):
    """Print error message."""
    return print(Panel(msg, style="red bold"))
