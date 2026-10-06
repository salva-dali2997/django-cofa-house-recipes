# TODO

## Deploy legacy Rails data to production

- [ ] Copy `local-copy.db` to somewhere the Fly machine can reach it, e.g.:
      `fly ssh sftp shell` then `put local-copy.db /tmp/local-copy.db`
      (or `fly ssh console` + `curl`/`scp` if that's easier)
- [ ] Run the import against production:
      `fly ssh console -C "python manage.py import_legacy_data --path /tmp/local-copy.db"`
      (goes through the same `DATABASE_URL`-based Django ORM connection as local — hits
      Postgres in prod automatically, no code changes needed)
- [ ] Spot-check the result: recipe/ingredient/comment/menu counts, a couple of directions
      fields, a comment's "time ago" render
- [ ] Delete `/tmp/local-copy.db` from the Fly machine afterward — it has a real email +
      password hash in it, don't leave it sitting on the server
- [ ] The import command is idempotent (`get_or_create`-based), so it's safe to re-run if
      something looks wrong the first time
- [ ] The import will also recreate the 3 historical menus (2026-08-02, 2026-08-16,
      2026-09-20) from `local-copy.db`, same as it did locally. We deliberately deleted
      those locally rather than fixing `_get_menu()` (see below) — do the same in prod
      after importing:
      ```python
      # via `fly ssh console -C "python manage.py shell"`
      from recipes.models import Menu
      Menu.objects.exclude(id=<the pre-existing prod menu's id>).delete()
      ```
      (check `Menu.objects.values('id', 'date')` first to confirm which id to keep)
