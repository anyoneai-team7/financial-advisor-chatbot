FROM python:3.8-slim as base

ARG UID
ARG GUNICORN_TIMEOUT=30
ENV G_TIMEOUT=$GUNICORN_TIMEOUT

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Append /home/app/.local/bin/ to PATH variable because
# gunicorn is installed there.
ENV PYTHONPATH=$PYTHONPATH:/app/
ENV PATH=$PATH:/home/app/.local/bin/


RUN adduser -u $UID --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

EXPOSE 5000

FROM base as develop
CMD [ "python", "./app.py" ]

FROM base as test
RUN ["pytest", "-v", "./tests"]

FROM base as production
ENTRYPOINT gunicorn --timeout=$G_TIMEOUT --workers=4 --bind 0.0.0.0:5000  app:app 