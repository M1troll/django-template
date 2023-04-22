# Setup

## Python Requirements

Currently, we're using `python 3.11`

The simplest way to configure proper Python version and virtual environment
is using [`pyenv`](https://github.com/pyenv/pyenv) and
[`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv).

Interpreter may be configured using

```
pyenv virtualenv-delete --force django-template
pyenv install 3.11 --skip-existing
pyenv virtualenv `pyenv latest 3.11` django-template
pyenv local django-template
pyenv shell django-template
```

After preparing virtual env need to install tools for preparing project.

```console
pip install -r requirements/local_build.txt
```

```
inv project.init
```
