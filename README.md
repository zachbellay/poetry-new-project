

poetry-new-project
==================

This is a small CLI utility meant to make it easier to set up a new Python project using Poetry and Pyenv.



## Quickstart 🚀

0. Prerequisite: Pyenv is already installed and configured on your system. If not, see [pyenv installer](https://github.com/pyenv/pyenv-installer).

1. Install the package: `pip install poetry-new-project`

2. Create a new project directory and cd into it: `mkdir my-new-project && cd my-new-project`

2. Create a new pyenv environment + poetry project : `poetry-new-project my-new-project-venv --version=3.10.6`

3. Wait for any python downloads to complete and finish the interactive poetry setup process.

4. Code! 🎉

## Inspiration (and why) 🤔

[Blog Post: Pyenv & Poetry New Project Start](https://zachbellay.com/posts/pyenv-poetry-new-project-start/)

Over the past year or so I have found myself referencing this blog post many times to start a new python project. 

This project is meant to supplant running (most) of these commands manually and to turn it into one CLI utility.

```bash
# install pyenv on your machine

curl https://pyenv.run | bash

# install python in pyenv

pyenv install 3.9.5

# create virtual environment:

pyenv virtualenv 3.9.5 hotdog-not-hotdog

# set hotdog-not-hotdog as the default virtual environment for the current directory

pyenv local hotdog-not-hotdog

# install poetry in your virtual environment

pip install poetry

# initialize project

poetry init

# install new dependencies

poetry add numpy

# install dependencies (if a pyproject.toml + poetry.lock already exists for a project)

poetry install
```

## Build 🛠

```bash

    poetry build

```

## Publish 📖

_Note:_ Remember to update the version in `pyproject.toml` when publishing a new version.

```bash

    poetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD

```

## Formatting ✨

```bash

    black poetry_new_project

```

## License 📜
This project is licensed under the terms of the MIT license, see MIT - see `License file <LICENSE>`_.



# TODO

- [] - Write test cases (should run inside of Docker container)
    - starting case: base python image, no pyenv etc
        - test case 1: create virtual environment
            - poetry-new-project test1 --version 3.9.5
        - test case 2: create same virtual environment and expect failure because it is not forced
            - poetry-new-project test1 --version 3.9.5
            - assert fail
        - test case 3: create same virtual environment with force flag and ensure that environment is re-created
            - poetry-new-project test1 --version 3.9.5 --force
        - write tox test to test multiple versions of python, especially earlier versions (i.e. 3.5) since the current setting is only 3.9+
- [] - write CI/CD pipeline
    - [] - create github action to push successfully built project to pypi
    - [] - create github action to run test cases