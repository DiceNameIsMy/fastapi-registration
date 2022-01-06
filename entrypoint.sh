#!/bin/sh

pipenv run alembic upgrade head

exec "$@"
