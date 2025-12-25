FROM python:3.13.11-alpine3.23
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apk add --no-cache libstdc++ gcc g++ musl-dev

COPY . /app

WORKDIR /app
RUN uv sync --frozen
# RUN uv sync --frozen --no-cache

EXPOSE 8000

# CMD ["uv", "run", "app/app.py", "--port", "80", "--host", "0.0.0.0"]
CMD ["uv", "run", "runner.py"]
