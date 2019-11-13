FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get -y install gettext
RUN pip install --upgrade pip

RUN mkdir /confs
WORKDIR /confs
ADD requirements.txt .
RUN pip install -r requirements.txt

ARG APP_DIR=/src
WORKDIR ${APP_DIR}

RUN mkdir /static
