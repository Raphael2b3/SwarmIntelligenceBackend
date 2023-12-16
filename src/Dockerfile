FROM python:3.12-alpine
LABEL authors="Raphael2b3"

ADD requirements.txt ./


RUN apk add gcc

RUN apk add libffi-dev

RUN apk add curl

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN rm -f ./requirements.txt

ADD . ./src

WORKDIR ./src

CMD ["python", "main.py"]
