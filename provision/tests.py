from invoke import task

from . import django


@task
def run(
    context,
    path="apps libs",
    parallel=True,
    keepdb=True,
    tags="--exclude-tag slow "
    "--exclude-tag model_unimportant "
    "--exclude-tag slow_admin",
):
    """Run django tests with ``extra`` args for ``p`` tests.

    ``p`` means ``params`` - extra args for tests

    """
    extras = []
    if keepdb:
        extras.append("--keepdb")
    if parallel:
        extras.append("--parallel")
    django.manage(context, " ".join(["test", path, tags, " ".join(extras)]))
