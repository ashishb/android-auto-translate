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

install:
	poetry install

docker_lint:
	hadolint Dockerfile

python_lint:
	# stop the build if there are Python syntax errors or undefined names
	poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	poetry run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	poetry run black . -S

python_test:
	poetry run pytest

lint: docker_lint python_lint

test: python_test
