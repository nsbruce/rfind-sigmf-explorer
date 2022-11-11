FROM ubuntu:22.04

ENV container docker PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
        python3.10 \
        python3-venv \
        ipython3 && \
    apt-get clean

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.2.0 python3 -
ENV PATH "$PATH:/root/.local/bin"
RUN poetry config virtualenvs.create false

