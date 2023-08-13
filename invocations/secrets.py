import shutil
from pathlib import Path

from invoke import task

from . import common


@task
def create_env_template(
    context,
    override=False,
    template=".env.template",
    to=".env",
    dir="config/settings/",
):
    """Prepare .env file for environment variables from template."""
    common.print_success("Create .env file from template")
    template_path, env_path = Path(dir + template), Path(dir + to)
    if override or not env_path.exists():
        shutil.copyfile(template_path, env_path)
        common.print_warn(f"You need to set environment variables in {env_path}")
