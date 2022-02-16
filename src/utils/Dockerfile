FROM python:3.8-slim

# to install python package psycopg2 (for postgres)
RUN apt-get update
RUN apt-get install -y postgresql libpq-dev postgresql-client postgresql-client-common gcc

# add user (change to whatever you want)
# prevents running sudo commands
RUN useradd -r -s /bin/bash anthony

# set current env
ENV HOME /app
WORKDIR /app
ENV PATH="/app/.local/bin:${PATH}"

RUN chown -R anthony:anthony /app
USER anthony

# set app config option
ENV FLASK_ENV=production


# AWS RDS vars
ARG POSTGRES_USER
ARG POSTGRES_PW
ARG POSTGRES_URL
ARG POSTGRES_DB

ENV POSTGRES_USER $POSTGRES_USER
ENV POSTGRES_PW $POSTGRES_PW
ENV POSTGRES_URL $POSTGRES_URL
ENV POSTGRES_DB $POSTGRES_DB

# Avoid cache purge by adding requirements first
ADD ./requirements.txt ./requirements.txt

RUN pip3 install --no-cache-dir -r ./requirements.txt --user

# Add the rest of the files
COPY . /app
WORKDIR /app

# start web server
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers=5"]