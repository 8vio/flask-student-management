FROM docker.io/python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_SETTINGS_MODULE=config.default
ENV FLASK_APP=entrypoint:app
ENV FLASK_ENV="production"

WORKDIR /app

RUN apt-get -qq update \
    && apt-get install -y -qq libpq-dev python3.8-dev \
    && apt-get -qq clean \
    && rm -fr /var/lib/apt/lists/*

COPY . .
RUN pip install -q -r requirements/production.txt

EXPOSE 3001

RUN chmod u+x ./docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
