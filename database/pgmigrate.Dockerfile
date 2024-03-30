FROM python:3.10-slim-bullseye

WORKDIR /pgmigrate

COPY ./migrations /pgmigrate/migrations

RUN apt-get update \
  && apt-get install -y --no-install-recommends python3-dev libpq-dev gcc \
  && rm -rf /var/lib/apt/lists/* \
  && pip install yandex-pgmigrate

ENV POSTGRES_CONNECTION_STRING=

ENTRYPOINT pgmigrate -t latest -c "$POSTGRES_CONNECTION_STRING" migrate
