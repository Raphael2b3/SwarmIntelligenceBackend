FROM rust:slim
LABEL authors="Raphael2b3"


ADD requirements.txt ./


RUN apt-get update

RUN apt-get install -y python3-full

RUN python3 -m venv .venv

RUN .venv/bin/python -m pip install --upgrade pip

RUN .venv/bin/python -m pip install -r requirements.txt

ADD . .


CMD [".venv/bin/python", "main.py"]
