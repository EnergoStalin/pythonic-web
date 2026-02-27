FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml .
RUN uv sync

COPY src ./src

COPY docker-entrypoint.sh .

ENTRYPOINT ["./docker-entrypoint.sh", "uv", "run", "fastapi", "run", "src/api/main.py"]
