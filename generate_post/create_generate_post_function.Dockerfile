# FROM https://medium.com/@gotraveltoworld/use-docker-to-develop-the-aws-lambda-python-3-6-525007907369
FROM lambci/lambda:build-python3.6

WORKDIR /var/task

# boto3 layer
RUN pip install --compile --no-cache-dir -t tmp/python/lib/python3.6/site-packages boto3 && \
    cd tmp && \
    zip -r9 ../boto3.zip . && \
    cd .. && \
    rm -rf tmp/

# nlp layer
RUN pip install --compile --no-cache-dir -t tmp/python/lib/python3.6/site-packages markovify nltk && \
    cd tmp && \
    zip -r9 ../nlp.zip . && \
    cd .. && \
    rm -rf tmp/

# http-client layer
RUN pip install --compile --no-cache-dir -t tmp/python/lib/python3.6/site-packages requests oauth2 && \
    cd tmp && \
    zip -r9 ../http-client.zip . && \
    cd .. && \
    rm -rf tmp/

# nltk-data layer
RUN pip install nltk && \
    mkdir -p tmp/ && \
    python -c "import nltk; nltk.download('averaged_perceptron_tagger', download_dir='tmp/nltk_data'); nltk.download('gutenberg', download_dir='tmp/nltk_data');" && \
    cd tmp && \
    zip -r9 ../nltk-data.zip . && \
    cd .. && \
    rm -rf tmp/

# lambda function
COPY generate_post.py .
COPY tumblr_client.py .
COPY generate_post/lambda_function.py .
RUN zip -r9 lambda.zip *.py

CMD echo "Nothing to do."