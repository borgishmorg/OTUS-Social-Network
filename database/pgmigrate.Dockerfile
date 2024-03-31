FROM python:3.10-slim-bullseye

WORKDIR /pgmigrate

RUN apt-get update \
  && apt-get install -y --no-install-recommends python3-dev libpq-dev gcc \
  && rm -rf /var/lib/apt/lists/* \
  && pip install yandex-pgmigrate

COPY ./migrations /pgmigrate/migrations

ARG DB_CONN

ENTRYPOINT pgmigrate -t latest -c "$DB_CONN" migrate
