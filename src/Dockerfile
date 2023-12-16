FROM python:latest
LABEL authors="Raphael2b3"

ADD requirements.txt ./

RUN pip install --upgrade pip

RUN curl https://sh.rustup.rs -sSf | bash -s -- -y

RUN pip install -r requirements.txt

RUN rm -f ./requirements.txt

ADD . ./src

WORKDIR ./src

CMD ["python", "main.py"]
