import sqlite3
from datetime import timezone as dt_timezone, datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from recipes.models import Recipe, Ingredient, RecipeIngredient, Comment, Menu


def _aware(sqlite_datetime_str):
  naive = datetime.fromisoformat(sqlite_datetime_str)
  return timezone.make_aware(naive, dt_timezone.utc)


class Command(BaseCommand):
  help = "One-time import of recipes/ingredients/comments/menus from the legacy Rails sqlite dump."

  def add_arguments(self, parser):
    parser.add_argument("--path", default="local-copy.db", help="Path to the legacy Rails sqlite file.")

  def handle(self, *args, **options):
    conn = sqlite3.connect(options["path"])
    conn.row_factory = sqlite3.Row

    recipe_id_map = {}  # rails recipe id -> Django Recipe instance
    recipes_created = 0
    for row in conn.execute("SELECT id, name, instructions, created_at FROM recipes"):
      recipe, created = Recipe.objects.get_or_create(
        name=row["name"], defaults={"directions": row["instructions"]}
      )
      if created:
        Recipe.objects.filter(pk=recipe.pk).update(created_at=_aware(row["created_at"]))
        recipes_created += 1
      recipe_id_map[row["id"]] = recipe

    ingredients_created = 0
    for row in conn.execute("SELECT name, quantity, recipe_id FROM ingredients"):
      recipe = recipe_id_map.get(row["recipe_id"])
      if recipe is None:
        continue  # orphaned row safety net
      ingredient, _ = Ingredient.objects.get_or_create(name=Ingredient.normalize(row["name"]))
      _, created = RecipeIngredient.objects.get_or_create(recipe=recipe, ingredient=ingredient, quantity=row["quantity"])
      ingredients_created += created

    comments_created = 0
    for row in conn.execute("SELECT name, comment, recipe_id, created_at FROM feedbacks"):
      recipe = recipe_id_map.get(row["recipe_id"])
      if recipe is None:
        continue
      content = f'{row["name"]}: {row["comment"]}' if row["name"] else row["comment"]
      comment, created = Comment.objects.get_or_create(recipe=recipe, content=content)
      if created:
        Comment.objects.filter(pk=comment.pk).update(created_at=_aware(row["created_at"]))
        comments_created += 1

    menu_id_map = {}
    menus_created = 0
    for row in conn.execute("SELECT id, date FROM menus"):
      menu, created = Menu.objects.get_or_create(date=row["date"])
      menu_id_map[row["id"]] = menu
      menus_created += created

    menu_links_created = 0
    for row in conn.execute("SELECT menu_id, recipe_id FROM menu_recipes"):
      recipe = recipe_id_map.get(row["recipe_id"])
      menu = menu_id_map.get(row["menu_id"])
      if recipe and menu and not recipe.menu.filter(pk=menu.pk).exists():
        recipe.menu.add(menu)
        menu_links_created += 1

    conn.close()

    self.stdout.write(self.style.SUCCESS(
      f"Recipes: {recipes_created} created ({len(recipe_id_map)} total in file). "
      f"Ingredients: {ingredients_created} new recipe-ingredient links. "
      f"Comments: {comments_created} created. "
      f"Menus: {menus_created} created ({len(menu_id_map)} total in file), "
      f"{menu_links_created} new menu-recipe links."
    ))
