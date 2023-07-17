# Beaver
**TBD**


# Usage Guide
**TBD**: installation, pre-setup, running on docker

# Development Guide

To setup your local environment you need **Python 3.11+** installed locally or [asdf](https://asdf-vm.com/).

If you are using `asdf` follow the steps below:

```bash
asdf install
python -m venv venv
source venv/bin/activate
pip install taskipy
```

>  In case you already have **Python 3.11** installed you can skip the first command.

Once the `virtualenv` is created and `taskipy` installed, you can run `task dependencies`
to install all dependencies (including development dependencies) defined in the `pyproject.yaml`.

Other tasks:

* `task test`
* `task mypy`
* `task lint`
* `task format`
* `task build`
* `task dependencies`
* `task -l`

