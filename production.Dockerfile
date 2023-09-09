FROM python:alpine
LABEL authors="Raphael2b3"
WORKDIR /app
ADD production.requirements.txt ./

RUN pip install -r production.requirements.txt

RUN rm -f ./production.requirements.txt

CMD ["python", "main.py"]
