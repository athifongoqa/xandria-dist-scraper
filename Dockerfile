FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
COPY requirements.txt ./requirements.txt

RUN pip3 install --upgrade pip
RUN python3 -m pip install -r requirements.txt

COPY . /app

EXPOSE 8000