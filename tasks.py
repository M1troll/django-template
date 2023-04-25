import inspect

# hack to support `invoke` for python 3.11
# https://github.com/pyinvoke/invoke/issues/833
if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec

from invoke import Collection

from provision import (
    django,
    docker,
    git,
    linters,
    project,
    secrets,
    start,
    tests,
)

ns = Collection(
    django,
    git,
    linters,
    project,
    start,
    secrets,
    tests,
    docker,
)

# Configurations for run command
ns.configure({"run": {"pty": True, "echo": True}})
