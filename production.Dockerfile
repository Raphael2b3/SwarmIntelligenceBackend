FROM raphael2b3/swarmintelligencebackend:base
LABEL authors="Raphael2b3"
WORKDIR /app

ADD src/ ./src
WORKDIR ./src

CMD ["python", "main.py"]
