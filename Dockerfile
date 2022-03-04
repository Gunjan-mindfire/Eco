FROM python:3.8

ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get update && apt-get install -y libmariadb-dev gcc
RUN mkdir /app
WORKDIR /app
COPY . /app/
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt
EXPOSE 8000