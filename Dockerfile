# --- Stage 1: build frontend assets with Vite ---
FROM node:22-slim AS assets

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY vite.config.js ./
COPY assets ./assets
RUN npm run build

# --- Stage 2: Python app ---
FROM python:3.14-slim AS app

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --group prod --no-install-project

COPY . .
COPY --from=assets /app/static ./static
RUN uv sync --frozen --no-dev --group prod

ENV PATH="/app/.venv/bin:$PATH"

# Only needed so `collectstatic` can import settings at build time -
# no real secrets or DB access are required for this step.
RUN SECRET_KEY=collectstatic-build-only python manage.py collectstatic --noinput

RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "cofa_house_recipes.wsgi:application", "--bind", "0.0.0.0:8000"]
