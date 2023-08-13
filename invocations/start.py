__all__ = (
    "run_local_python",
)


def run_local_python(context, command: str, watchers=()):
    """Run command using local python interpreter."""
    return context.run(
        " ".join(["python3", command]),
        watchers=watchers,
    )


def run_python(*args, **kwargs):
    """Run command in different interpeter depdending on .invoke config."""
    run_local_python(*args, **kwargs)
