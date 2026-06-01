FROM python:3.12-slim AS base

FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim AS builder

WORKDIR /app
# Only copy uv.lock and not pyproject.toml
# This ensures hermiticity of the build
# And prevents docker image invalidation in case non-dependency changes
# are made to pyproject.toml
COPY uv.lock /app
# Install dependencies
# virtual env is created in "/app/.venv" directory
RUN uv init --name src && uv sync --no-dev --frozen

FROM base AS runner
COPY src /app/src
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app/.venv/lib/python3.12/site-packages
# Code file to execute when the docker container starts up
ENTRYPOINT ["/app/src/translations.py"]
