FROM python:3.7

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en
RUN python -c "import nltk; nltk.download('averaged_perceptron_tagger'); nltk.download('gutenberg');"

VOLUME /usr/src/app/settings.py
VOLUME /usr/src/app/text_source.txt