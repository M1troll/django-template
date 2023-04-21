import os

from invoke import task

from . import common, django, docker, git, tests

# ------------------------------------------------------------------------------
# Build project locally
# ------------------------------------------------------------------------------


@task
def copy_local_settings(context, force_update=True):
    """Copy local settings from template.

    Args:
        force_update(bool): rewrite file if exists or not

    """
    local_settings = "config/settings/local.py"
    local_template = "config/settings/local.template.py"

    if force_update or not os.path.isfile(local_settings):
        context.run(" ".join(("cp", local_template, local_settings)))


@task
def copy_vscode_settings(context, force_update=False):
    """Copy vscode settings from template.

    Args:
        force_update(bool): rewrite file if exists or not

    """
    local_settings = ".vscode/settings.json"
    local_template = ".vscode/recommended_settings.json"

    if force_update or not os.path.isfile(local_settings):
        context.run(" ".join(("cp", local_template, local_settings)))


@task
def init(context, clean=False):
    """Build project from scratch."""
    common.print_success("Setting up git config")
    git.setup(context)
    if clean:
        docker.clear(context)
    copy_local_settings(context)
    copy_vscode_settings(context)
    install_requirements(context)
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
