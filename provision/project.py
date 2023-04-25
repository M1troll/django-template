from invoke import task

from . import common, django, docker, git, tests

# ------------------------------------------------------------------------------
# Build project locally
# ------------------------------------------------------------------------------


@task
def init(context, clean=False):
    """Build project from scratch."""
    common.print_success("Setting up git config")
    git.setup(context)
    if clean:
        docker.clear(context)

    # Now we use docker container for work with running project
    # so we don't need to install requirements locally
    # install_requirements(context)

    # Build container
    docker.build(context)

    django.migrate(context)
    tests.run(context)
    django.createsuperuser(context)
    skip_checks = "check-migrations,swagger-dump,tests,swagger-relevance"
    git.run_hooks(context, to_skip=skip_checks)


# ------------------------------------------------------------------------------
# Manage dependencies
# ------------------------------------------------------------------------------


@task
def upgrade_pip(context):
    """Upgrade pip version."""
    common.print_success("Upgrade pip")
    context.run("python3.11 -m pip install --upgrade pip")


@task
def install_requirements(context, env="development"):
    """Install local development requirements."""
    upgrade_pip(context)
    common.print_success(f"Install requirements from {env}.txt")
    context.run(f"pip install -r requirements/{env}.txt")


@task
def pip_compile(context, update=False):
    """Compile requirements with pip-compile."""
    common.print_success("Compile requirements with pip-compile")
    upgrade = "-U" if update else ""
    in_files = [
        "production.in",
        "development.in",
    ]
    for in_file in in_files:
        with context.cd("requirements"):
            context.run(f"pip-compile -q {in_file} {upgrade}")
    if update:
        context.run("pre-commit autoupdate")
