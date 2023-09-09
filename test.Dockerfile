FROM raphael2b3/swarmintelligencebackend:production
LABEL authors="Raphael2b3"
WORKDIR /app
ADD tests/ ./
ADD test.requirements.txt ./

RUN pip install -r test.requirements.txt

RUN rm -f ./test.requirements.txt


CMD ["pytest"]