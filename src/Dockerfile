FROM python:latest
LABEL authors="Raphael2b3"

ADD requirements.txt ./

RUN pip install --upgrade pip

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y

RUN pip install -r requirements.txt

RUN rm -f ./requirements.txt

ADD . ./src

WORKDIR ./src

CMD ["python", "main.py"]
