FROM python:3.9-slim as builder

ENV PYTHONUNBUFFERED 1
WORKDIR /mad

RUN apt-get update -qq && apt-get install --no-install-recommends curl gnupg2 gcc python3-dev libpq-dev python3-wheel \
    python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev \
    shared-mime-info musl-dev libsdl-pango-dev -y

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH "$PATH:/root/.poetry/bin/"

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . /mad
