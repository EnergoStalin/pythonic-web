FROM python:3.11-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml .
RUN uv sync

COPY src ./src

ENTRYPOINT ["uv", "run", "fastapi", "run", "src/api/main.py"]
