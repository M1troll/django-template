from invoke import Exit, UnexpectedExit, task

from .common import print_error, print_success

##############################################################################
# Linters
##############################################################################


DEFAULT_FOLDERS = " ".join([
    "apps",
    "provision",
])


@task
def all(context, path=DEFAULT_FOLDERS):
    """Run all linters not covered by pre-commit.

    Args:
        context: Invoke's context
        path(str): Path to selected file

    Usage:
        # is simple mode without report
        inv linters.all
        # usage on selected file
        inv linters.all --path='apps/users/models.py'

    """
    print_success("Linters: running all linters")
    linters = (
        dead_fixtures,
        mypy,
    )
    failed = []
    for linter in linters:
        try:
            linter(context, path)
        except UnexpectedExit:
            failed.append(linter.__name__)
    if failed:
        print_error(
            f"Linters failed: {', '.join(map(str.capitalize, failed))}",
        )
        raise Exit(code=1)


@task
def dead_fixtures(context, path=DEFAULT_FOLDERS):
    """Lint not used fixtures, see https://github.com/jllorencetti/pytest- deadfixtures."""
    return context.run(command=f"pytest {path} --dead-fixtures")


@task
def mypy(context, path=DEFAULT_FOLDERS):
    """Lint code with mypy."""
    return context.run(command=f"mypy {path}")
