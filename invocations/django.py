from invoke import FailingResponder, Failure, Responder, task

from . import common, docker, start


def wait_for_database(context):
    """Ensure that database is up and ready to accept connections.

    Function called just once during subsequent calls of management commands.

    """
    if hasattr(wait_for_database, "_called"):
        return
    docker.up(context)
    wait_for_database._called = True    # type: ignore[attr-defined]


@task
def manage(context, command, watchers=()):
    """Run ``manage.py`` command.

    This command also handle starting of required services and waiting DB to
    be ready

    Args:
        context: Invoke context
        command: Manage command
        watchers: Automated responders to command

    """
    wait_for_database(context)
    return start.run_python(
        context,
        " ".join(["manage.py", command]),
        watchers=watchers,
    )


@task
def makemigrations(context):
    """Run makemigrations command and chown created migrations."""
    common.print_success("Django: Make migrations")
    manage(context, "makemigrations")


@task
def check_new_migrations(context):
    """Check if there is new migrations or not."""
    common.print_success("Checking migrations")
    manage(context, "makemigrations --check --dry-run")


@task
def migrate(context):
    """Run ``migrate`` command."""
    common.print_success("Django: Apply migrations")
    manage(context, "migrate")


@task
def resetdb(context, apply_migrations=True):
    """Reset database to initial state (including test DB)."""
    common.print_success("Reset database to its initial state")
    manage(context, "drop_test_database --noinput")
    manage(context, "reset_db -c --noinput")
    if not apply_migrations:
        return
    migrate(context)
    createsuperuser(context)


@task
def createsuperuser(
    context,
    email="root@root.com",
    username="root",
    password="root",
):
    """Create superuser."""
    common.print_success("Create superuser")
    responder_email = FailingResponder(
        pattern=r"Email address: ",
        response=email + "\n",
        sentinel="That Email address is already taken.",
    )
    responder_user_name = Responder(
        pattern=r"Username: ",
        response=username + "\n",
    )
    responder_password = Responder(
        pattern=r"(Password: )|(Password \(again\): )",
        response=password + "\n",
    )

    try:
        manage(
            context,
            command="createsuperuser --noinput",
            watchers=[
                responder_email,
                responder_user_name,
                responder_password,
            ],
        )
    except Failure:
        common.print_warn("Superuser with that email already exists. Skipped.")


@task
def run(context):
    """Run development web-server."""
    common.print_success("Running server")
    # We use ``0.0.0.0:8000`` instead of ``localhost`` or ``127.0.0.1``
    # because docker use these addresses for its loopback
    # https://stackoverflow.com/questions/49476217/docker-cant-access-django-server
    docker.docker_compose_run(
        context,
        params="--rm --service-ports",
        container="web",
        command="python3 manage.py runserver_plus 0.0.0.0:8000",
    )


@task
def shell(context, params=None):
    """Shortcut for manage.py shell_plus command.

    Additional params available here:
        https://django-extensions.readthedocs.io/en/latest/shell_plus.html

    """
    common.print_success("Entering Django Shell")
    manage(context, "shell_plus --ipython {}".format(params or ""))
