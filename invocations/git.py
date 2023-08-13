from invoke import Exit, UnexpectedExit, task

from . import common


@task
def install_pre_commit(context):
    """Install git hooks via pre-commit."""
    common.print_success("Setting up pre-commit")
    # Remove previously installed hooks
    context.run("git config --unset-all core.hooksPath", warn=True)
    hooks = " ".join(
        f"--hook-type {hook}" for hook in (
            "pre-commit",
            "pre-push",
            "commit-msg",
        )
    )
    context.run(f"pre-commit install {hooks}")


@task
def setup(context):
    """Set up git for working."""
    install_pre_commit(context)
    # https://wiki.saritasa.rocks/general/git/#fast-forward-merges
    context.run("git config --add merge.ff false")
    # https://wiki.saritasa.rocks/general/git/#auto-merged-pulls
    context.run("git config --add pull.ff only")


@task
def run_hooks(context, to_skip="tests,swagger-relevance"):
    """Run git hooks."""
    common.print_success("Running git hooks")
    params = f"SKIP={to_skip} " if to_skip else ""

    try:
        context.run(f"{params}pre-commit run --hook-stage push --all-files")
    except (UnexpectedExit, Exit) as hooks_exit:
        common.print_error("Found some errors\nPLS fix them!")
        raise hooks_exit
    common.print_success("Wonderful JOB! Thank You!")
