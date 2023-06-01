FROM python:3.8-slim

ARG UID
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN adduser -u $UID --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

EXPOSE 5000

CMD [ "python", "./app.py" ]