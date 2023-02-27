# Build using
# DOCKER_BUILDKIT=1 docker build -f Dockerfile ..
# Container image that runs your code
FROM python:3.11-alpine

COPY ./requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r /requirements.txt
# Copies your code file from your action repository to the filesystem path `/` of the container
COPY ./src /src

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/src/translations.py"]
