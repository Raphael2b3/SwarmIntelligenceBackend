FROM python:3.12-slim
LABEL authors="Raphael2b3"

ADD requirements.txt ./

RUN pacman -S gcc

RUN pacman -S libffi-dev

RUN pacman -S curl

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN rm -f ./requirements.txt

ADD . ./src

WORKDIR ./src

CMD ["python", "main.py"]
