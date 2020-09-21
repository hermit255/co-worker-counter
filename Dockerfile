FROM python:3
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING utf-8
RUN mkdir /script /app
WORKDIR /script
COPY requirements.txt /script/
RUN pip install -r requirements.txt
WORKDIR /app