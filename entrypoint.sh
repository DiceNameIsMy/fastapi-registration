#!/bin/sh

pipenv run alembic upgrade head

pipenv run pytest

exec "$@"
