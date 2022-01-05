#!/bin/sh

pipenv run alembic upgrade head

export DB_FAKE=1
pipenv run pytest -vv
export DB_FAKE=0

exec "$@"
