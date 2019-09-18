FROM python:3.7.3-alpine3.9

ENV FLASK_APP=manifesto.app.py

RUN apk update \
    && apk add ca-certificates wget \
    && update-ca-certificates

RUN apk add --no-cache \
    postgresql-dev \
    g++ \
    gcc

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app

CMD exec gunicorn -w 5 --timeout=500 --reload -b 0.0.0.0:5000 manifesto.wsgi:app
