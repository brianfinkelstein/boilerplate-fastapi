# code
lint:
    pre-commit-validate-config
fmt:
    black .

# local tasks
python-run:
    poetry run uvicorn app.main:app --reload
python-test:
    poetry run pytest

initial-setup:
    brew install pyenv

    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
    source $HOME/.poetry/env
    pyenv install 3.10.0

    poetry env use ~/.pyenv/versions/3.10.0/bin/python3
    poetry install
