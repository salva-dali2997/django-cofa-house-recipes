#!/bin/sh
set -e

python manage.py migrate --noinput

# Only for local dev (set by docker-compose.yml) - never run these against production.
if [ "$CREATE_SUPERUSER" = "true" ]; then
    python manage.py ensure_superuser
fi

if [ "$SEED_RECIPES" = "true" ]; then
    python manage.py seed_recipes
fi

exec "$@"
