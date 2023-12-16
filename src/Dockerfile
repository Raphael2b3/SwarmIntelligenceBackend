FROM python:3.12-alpine
LABEL authors="Raphael2b3"

ADD requirements.txt ./

RUN apk add gcc

RUN apk add libffi-dev

RUN wget -O init.sh https://sh.rustup.rs
RUN sh init.sh -y
RUN cp $HOME/.cargo/bin/* /usr/local/bin

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN rm -f ./requirements.txt

ADD . ./src

WORKDIR ./src

CMD ["python", "main.py"]
