FROM python:3.9.9-slim

# install initial dependencies
RUN pip install --no-cache --upgrade pip pipenv

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1
ENV APP_HOME=/app

WORKDIR ${APP_HOME}

# install dependencies
COPY Pipfile.lock Pipfile ./
RUN pipenv install

# copy entrypoint
COPY entrypoint.sh /run/entrypoint.sh
RUN chmod +x /run/entrypoint.sh

# copy project
COPY src $APP_HOME

ENTRYPOINT [ "/run/entrypoint.sh" ]
