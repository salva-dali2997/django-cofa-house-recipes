# Cofa House Recipes

A Django app for managing recipes, with a Vite-built React frontend bundle served through Django's static files.

## Stack

- Django 6.1, managed with [uv](https://docs.astral.sh/uv/)
- Postgres in production/docker, SQLite for simple local dev
- React, bundled by Vite from `assets/` into `static/`
- Gunicorn + [WhiteNoise](https://whitenoise.readthedocs.io/) serve the app and its static files in production
- Deploys to Fly.io (see `fly.toml`)

## Project layout

- `cofa_house_recipes/` — Django project (settings, urls, wsgi)
- `recipes/` — the recipes app (models, views, templates)
- `templates/` — Django templates
- `assets/` — React frontend source (`.jsx` components), built by Vite
- `static/` — Vite's build output, plus any static assets checked straight into `static/css` and `static/images`
- `staticfiles/` — `collectstatic` output, generated at build/deploy time only (not checked in)

## Django ↔ React data flow

Views pass data to templates as plain context, same as before. Templates hand that data to React via
[`json_script`](https://docs.djangoproject.com/en/6.1/ref/templates/builtins/#json-script), which
safely serializes it into a `<script type="application/json">` tag. The React entrypoint
(`assets/index.jsx`) reads that tag and renders the app into `<div id="root">`.

See `recipes/views.py` (builds `recipes_data`), `templates/recipes/view_all.html`
(`{{ recipes_data|json_script:"recipes-data" }}`), and `assets/index.jsx` /
`assets/RecipeList.jsx` for the pattern to follow when adding new React-backed views.

## Local development — SQLite, no Docker

Requirements: Python 3.14, [uv](https://docs.astral.sh/uv/), Node 22+.

```bash
cp .env.example .env
uv sync --group dev
npm install

uv run python manage.py migrate
uv run python manage.py ensure_superuser
uv run python manage.py seed_recipes
npm run build -- --watch &
uv run python manage.py runserver
```

Leave `DATABASE_URL` unset in `.env` and the app falls back to `db.sqlite3` in the project root.

`ensure_superuser` creates a local superuser (`admin` / `admin`) if one doesn't already exist yet, so
you can log in to `/admin` right away. Override the username/password/email via the
`DJANGO_SUPERUSER_USERNAME` / `DJANGO_SUPERUSER_PASSWORD` / `DJANGO_SUPERUSER_EMAIL` env vars.

`seed_recipes` adds a handful of recipes, each with its own ingredients, so there's something 
to look at right away. It's safe to re-run — it skips any recipes that already exist by name, 
only adding ingredients that don't already exist for that recipe. Pass `--reset` to delete all 
existing recipes and ingredients first and reseed from scratch:

```bash
uv run python manage.py seed_recipes --reset
```

## Local development — Docker Compose (Postgres)

Requirements: Docker, Docker Compose. Uses Postgres instead of SQLite.

```bash
cp .env.example .env
docker compose up -d
```

This starts three services:

- `db` — Postgres
- `web` — Django dev server on http://localhost:8000, bind-mounted to your working copy
- `vite` — rebuilds `static/js` on change, so `web` picks up frontend changes on refresh

`entrypoint.sh` runs migrations on every `web` startup, and also runs `ensure_superuser` and
`seed_recipes` when `CREATE_SUPERUSER=true` / `SEED_RECIPES=true` (set in `docker-compose.yml`, not in
production). That means a local superuser (`admin` / `admin`) and sample recipes (with ingredients) are
ready without any extra steps. See the SQLite section above for how to override the superuser
credentials.

Run one-off management commands against the running stack, e.g.:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

## Production build

`Dockerfile` is a multi-stage build:

1. Installs frontend dependecies and runs `npm run build` to produce `static/`
2. Installs Python deps with `uv sync`
3. Runs `manage.py collectstatic` into `staticfiles/`, which WhiteNoise serves at runtime
4. Runs the app with `gunicorn`

```bash
docker build -t cofa-house-recipes .
docker run -p 8000:8000 --env-file .env cofa-house-recipes
```

## Run tests

Tests live in `recipes/tests.py`

```bash
uv run manage.py test recipes
```
