FROM python:3.12-slim

WORKDIR /usr/src/tbot

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /usr/src/tbot/app.py

ENTRYPOINT python app.py