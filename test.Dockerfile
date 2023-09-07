FROM python:alpine
LABEL authors="Raphael2b3"
WORKDIR /app
ADD src/ ./
ADD test.requirements.txt ./

RUN pip install -r test.requirements.txt

RUN rm -f ./test.requirements.txt


CMD ["python", "main.py"]