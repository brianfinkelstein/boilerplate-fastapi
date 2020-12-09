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
