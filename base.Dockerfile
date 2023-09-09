FROM python:alpine
LABEL authors="Raphael2b3"

ADD requirements.txt ./

RUN pip install -r requirements.txt

RUN rm -f ./requirements.txt

