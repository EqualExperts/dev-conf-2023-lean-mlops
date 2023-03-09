FROM python:3.10.10-slim-buster as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV POETRY_VERSION="1.1.13"
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1
ENV PYENV_NAME="taxi-analytics-env"

FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev curl build-essential
#RUN pip install pipenv
#RUN pip install "poetry==$POETRY_VERSION"
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
ENV PATH="${POETRY_HOME}/bin:${PATH}"

# Install python dependencies in /.venv
#COPY Pipfile .
#RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy
RUN mkdir /app
COPY poetry.lock /app
COPY pyproject.toml /app
WORKDIR /app
RUN poetry install --no-dev

