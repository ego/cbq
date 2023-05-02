# cbq - HTTP API

HTTP API for serving predictions.

## Installation

    pip install pipenv  # if you haven't already
    pipenv install
    pipenv run python app.py

## Development

    pipenv install --dev
    pipenv shell
    uvicorn app:app --reload


API URL

    http://127.0.0.1:8000
    http://127.0.0.1:8000/docs


## Test

    pytest

## Directory structure

    ├── Dockerfile            <- Dockerfile for HTTP API
    ├── Pipfile               <- The Pipfile for reproducing the serving environment
    ├── app.py                <- The entry point of the HTTP API
    └── tests
        ├── fixtures          <- Where to put example inputs and outputs
        │   ├── input.json    <- Test input data
        │   └── output.json   <- Test output data
        └── test_app.py       <- Integration tests for the HTTP API


## Tools

    pipenv upgrade
    pipenv update --dev
    pipenv lock

    pipenv run beautify
    pipenv run lint

    source $(pipenv --venv)/bin/activate
    `exit` or CTRL-d to exit the current subshell
