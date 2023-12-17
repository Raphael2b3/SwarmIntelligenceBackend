FROM python:3.12-slim
LABEL authors="Raphael2b3"

ADD requirements.txt ./


RUN apt-get update

RUN apt-get install build-essential libffi-dev curl -y

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN rm -f ./requirements.txt

ADD . ./src

WORKDIR ./src

CMD ["python", "main.py"]
