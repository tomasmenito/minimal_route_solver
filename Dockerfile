from python:3.9.1-slim-buster

ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-dev

ADD . /app

ENTRYPOINT ["poetry", "run", "cargo_truck"]
