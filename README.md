# American Sign Language Recognition System 

[Open source AI hackathon](https://lablab.ai/event/open-source-ai-hackathon/codebasequestions-cbq?channelId=1102943325432061963)

[Team Discord Channel](https://discord.com/channels/1068148026708860969/1102943325432061963)

A technology that will give the opportunity for people to communicate easily in their own language between one and other with more privacy and easier access.

Translate not only to understand what someone is saying but to understand what they are expressing thanks to the emotion recognition.


## Python Stack

* [Pipenv] for managing packages and virtualenvs in a modern way.
* [Prefect] for modern pipelines and data workflow.
* [Weights and Biases] for experiment tracking.
* [FastAPI] for self-documenting fast HTTP APIs - on par with NodeJS and Go - based on [asyncio], [ASGI], and [uvicorn].
* Modern CLI with [Typer].
* Batteries included: [Pandas], [numpy], [scipy], [seaborn], and [jupyterlab] already installed.
* Consistent code quality: [black], [isort], [autoflake], and [pylint] already installed.
* [Pytest] for testing.
* [GitHub Pages] for the public website.

## Quickstart

Install the latest Pipenv:

    pip install -U pipenv
    pipenv shell  # activates virtualenv

(Optional) Start Weights & Biases locally, if you don't want to use the cloud/on-premise version:

    wandb server start

Start working as ML/AI scientist:

    jupyter-lab


[Start working software engineering](serve/README.md):

	cd serve
	pipenv shell
	pipenv install --dev
	pipenv run uvicorn app:app --reload


* [Gradio frontend URL](http://127.0.0.1:8000)
* [Local API URL](http://127.0.0.1:8000/api)
* [Local DOCS URL](http://127.0.0.1:8000/docs)
* [Public GitHub Pages](http://ego.systemdef.com/cbq/)


## Directory structure

This is our your new project will look like:

    ├── .gitignore                <- GitHub's excellent Python .gitignore
    ├── LICENSE                   <- Project's license.
    ├── Pipfile                   <- The Pipfile for reproducing the analysis environment
    ├── README.md                 <- The top-level README for developers using this project.
    │
    ├── data
    │   ├── 0_raw                 <- The original, immutable data dump.
    │   ├── 0_external            <- Data from third party sources.
    │   ├── 1_interim             <- Intermediate data that has been transformed.
    │   └── 2_final               <- The final, canonical data sets for modeling.
    │
    ├── docs                      <- GitHub pages website
    │   ├── data_dictionaries     <- Data dictionaries
    │   └── references            <- Papers, manuals, and all other explanatory materials.
    │
    ├── notebooks                 <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                                the creator's initials, and a short `_` delimited description, e.g.
    │                                `01_cp_exploratory_data_analysis.ipynb`.
    │
    ├── output
    │   ├── features              <- Fitted and serialized features
    │   ├── models                <- Trained and serialized models, model predictions, or model summaries
    │   └── reports               <- Generated analyses as HTML, PDF, LaTeX, etc.
    │       └── figures           <- Generated graphics and figures to be used in reporting
    │
    ├── pipelines                 <- Pipelines and data workflows.
    │   ├── Pipfile               <- The Pipfile for reproducing the pipelines environment
    │   ├── pipelines.py          <- The CLI entry point for all the pipelines
    │   ├── <repo_name>           <- Code for the various steps of the pipelines
    │   │   ├──  __init__.py
    │   │   ├── etl.py            <- Download, generate, and process data
    │   │   ├── visualize.py      <- Create exploratory and results oriented visualizations
    │   │   ├── features.py       <- Turn raw data into features for modeling
    │   │   └── train.py          <- Train and evaluate models
    │   └── tests
    │       ├── fixtures          <- Where to put example inputs and outputs
    │       │   ├── input.json    <- Test input data
    │       │   └── output.json   <- Test output data
    │       └── test_pipelines.py <- Integration tests for the HTTP API
    │
    └── serve                     <- HTTP API for serving predictions
        ├── Dockerfile            <- Dockerfile for HTTP API
        ├── Pipfile               <- The Pipfile for reproducing the serving environment
        ├── app.py                <- The entry point of the HTTP API
        └── tests
            ├── fixtures          <- Where to put example inputs and outputs
            │   ├── input.json    <- Test input data
            │   └── output.json   <- Test output data
            └── test_app.py       <- Integration tests for the HTTP API


[Cookiecutter]: https://github.com/audreyr/cookiecutter
[Pipenv]: https://pipenv.pypa.io/en/latest/
[Prefect]: https://docs.prefect.io/
[Weights and Biases]: https://www.wandb.com/
[MLFlow]: https://mlflow.org/
[FastAPI]: https://fastapi.tiangolo.com/
[asyncio]: https://docs.python.org/3/library/asyncio.html
[ASGI]: https://asgi.readthedocs.io/en/latest/
[uvicorn]: https://www.uvicorn.org/
[Typer]: https://typer.tiangolo.com/
[Pandas]: https://pandas.pydata.org/
[numpy]: https://numpy.org/
[scipy]: https://www.scipy.org/
[seaborn]: https://seaborn.pydata.org/
[jupyterlab]: https://jupyterlab.readthedocs.io/en/stable/
[black]: https://github.com/psf/black
[isort]: https://github.com/timothycrosley/isort
[autoflake]: https://github.com/myint/autoflake
[pylint]: https://www.pylint.org/
[Pytest]: https://docs.pytest.org/en/latest/
[GitHub Pages]: https://pages.github.com/
[Git LFS]: https://git-lfs.github.com/
