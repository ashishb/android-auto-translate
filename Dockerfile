FROM python:3.12-slim as base

FROM base as builder
# Install Poetry
RUN pip install --no-cache-dir poetry==1.8.3
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
# virtual env is created in "/app/.venv" directory
ENV POETRY_NO_INTERACTION=1 \
POETRY_VIRTUALENVS_IN_PROJECT=1 \
POETRY_VIRTUALENVS_CREATE=true \
POETRY_CACHE_DIR=/tmp/poetry_cache
# Install dependencies
RUN --mount=type=cache,target=/tmp/poetry_cache poetry install --only main --no-root
RUN poetry install


FROM base as runner
COPY src /app/src
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/app/src/translations.py"]
