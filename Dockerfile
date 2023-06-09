# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.11.3-slim-bullseye

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
ENV PYTHONUNBUFFERED=1

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    git \
 && rm -rf /var/lib/apt/lists/*

# set the working directory
WORKDIR /app
# copy the repository files to it
COPY . /app
COPY requirements.* /app/

RUN pip install -U pip pip-tools wheel \
    && pip install -r requirements.txt

RUN python manage.py collectstatic --noinput --clear

# Port used by this container to serve HTTP.
EXPOSE 8000

# UWSGI
# See recommendations here: 
# https://www.bloomberg.com/company/stories/configuring-uwsgi-production-deployment/
CMD uwsgi --http=0.0.0.0:8000 --master --module=wsgi \
    --strict \
    --enable-threads \
    --single-interpreter \
    --need-app \
    --processes=3 \
    --threads=2 \
    --uid=1000 --gid=2000 \
    --harakiri=60 \
    --max-requests=5000 \
    --max-worker-lifetime=3600 \
    --reload-on-rss=450 \
    --worker-reload-mercy=60 \
    --vacuum \
    --die-on-term \
    --ignore-write-errors \
    --disable-write-exception