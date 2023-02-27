BINARY_NAME := "test-action"
DOCKER_TAG := "auto-translate-docker-action"

docker_build:
	DOCKER_BUILDKIT=1 docker build -t ${DOCKER_TAG} -f Dockerfile .
	echo "Created docker image with tag ${DOCKER_TAG} and size `$(MAKE) --quiet docker_print_image_size`"

# For local testing
docker_run: docker_build
	docker rm ${BINARY_NAME}; docker run --name ${BINARY_NAME} -p 127.0.0.1:80:80 \
		-it ${DOCKER_TAG}

docker_print_image_size:
	docker image inspect ${DOCKER_TAG} --format='{{.Size}}' | numfmt --to=iec-i

