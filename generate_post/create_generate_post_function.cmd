@SET IMAGE=screaming_bot_generate_post_image
@SET CONTAINER=screaming_bot_generate_post_container

docker build -t %IMAGE%:latest -f create_generate_post_function.Dockerfile ..
docker container rm %CONTAINER%
docker container create --name %CONTAINER% %IMAGE%:latest
rm -Rf build/
mkdir build
docker cp %CONTAINER%:/var/task/boto3.zip build/
docker cp %CONTAINER%:/var/task/nlp.zip build/
docker cp %CONTAINER%:/var/task/nltk-data.zip build/
docker cp %CONTAINER%:/var/task/http-client.zip build/
docker cp %CONTAINER%:/var/task/lambda.zip build/
docker rm %CONTAINER%