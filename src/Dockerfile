FROM python:3.12-alpine
LABEL authors="Raphael2b3"

ADD requirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt  --no-binary :none:

ADD . ./src

WORKDIR ./src

CMD ["python", "main.py"]
