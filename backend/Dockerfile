FROM python:3.10-slim-bullseye as python-base

ENV POETRY_VENV_PATH=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN python3 -m venv $POETRY_VENV_PATH \
    && $POETRY_VENV_PATH/bin/pip install -U pip setuptools \
    && $POETRY_VENV_PATH/bin/pip install poetry==1.8.2 \
    && $POETRY_VENV_PATH/bin/poetry install --only main

COPY backend ./backend
COPY scripts ./scripts

EXPOSE 8000
CMD [ "uvicorn", "backend:app", "--host=0.0.0.0", "--port=8000"]
