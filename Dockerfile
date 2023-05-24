FROM python:3.10.11 AS base
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PIP_ROOT_USER_ACTION=ignore

FROM base AS python-deps

ARG DEBIAN_FRONTEND=noninteractive


WORKDIR /build

RUN apt-get upgrade -y
RUN apt-get update && apt-get install -y --no-install-recommends gcc g++ libpq-dev curl zip
RUN pip3 install --upgrade pip
RUN pip3 install pipenv


RUN python -m venv .venv
COPY requirements.txt .
RUN #pip3 install -r requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt


FROM base AS runtime
WORKDIR /lean_mlops
COPY --from=python-deps /build/wheels /wheels
COPY --from=python-deps /build/requirements.txt .
RUN pip install --no-cache /wheels/*

WORKDIR /lean_mlops

EXPOSE 5000
EXPOSE 8888
CMD ["jupyter", "lab", "--port=8888", "--no-browser", "--allow-root", "--ip=0.0.0.0"]
