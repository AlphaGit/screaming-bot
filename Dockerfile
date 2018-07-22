FROM python:3.7.0-alpine3.8

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -m spacy download en
RUN python -c "import nltk; nltk.download('averaged_perceptron_tagger');"