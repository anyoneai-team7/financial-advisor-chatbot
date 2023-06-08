# syntax=docker/dockerfile:1
FROM python:3.9-slim as base

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH=$PYTHONPATH:/
ENV PATH=$PATH:/home/app/.local/bin/
#ARG UID

# Install pip requirements
ADD requirements.txt .
RUN pip install --upgrade pip
RUN --mount=type=cache,target=~/.cache/pip \
    pip install -r requirements.txt --default-timeout=1000

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
#RUN adduser -u $UID --disabled-password --gecos "" appuser && chown -R appuser /app
#USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
FROM base as build
CMD ["python", "main.py"]

FROM base as test
RUN ["pytest", "-v", "/app/tests"]