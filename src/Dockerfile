FROM python:3.12-alpine
LABEL authors="Raphael2b3"

ADD requirements.txt ./

RUN apk add build-base

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN rm -f ./requirements.txt

ADD . ./src

WORKDIR ./src

CMD ["python", "main.py"]
