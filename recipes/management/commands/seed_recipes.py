from django.core.management.base import BaseCommand

from recipes.models import Recipe, Ingredient

RECIPES = [
  {
    "name": "Watermelon Mint Salad",
    "ingredients": [
      {"name": "Watermelon", "quantity": "1"},
      {"name": "Mint", "quantity": "5 sprigs"},
      {"name": "Salt", "quantity": "2 tsp"},
      {"name": "Lemon", "quantity": "1"},
    ]
  },
  {
    "name": "Ants on a Log",
    "ingredients": [
      {"name": "Celery", "quantity": "5"},
      {"name": "Peanut Butter", "quantity": "5 tbsp"},
      {"name": "Raisins", "quantity": "1 bag"},
    ]
  },
  {
    "name": "Spaghetti",
    "ingredients": [
      {"name": "Pasta", "quantity": "1 box"},
      {"name": "Sauce", "quantity": "1 Can"},
    ]
  },
  {
    "name": "Grilled Cheese",
    "ingredients": [
      {"name": "Bread", "quantity": "2 slices"},
      {"name": "Cheese", "quantity": "1 cup"},
    ]
  },
  {
    "name": "Caesar Salad",
    "ingredients": [
      {"name": "Romaine Lettuce", "quantity": "1 Head"},
      {"name": "Parmesan Cheese", "quantity": "1/4 cup"},
      {"name": "Caesar Dressing", "quantity": "1/4 cup"},
    ]
  },
  {
    "name": "Tomato Soup",
    "ingredients": [
      {"name": "Tomatoes", "quantity": "5"},
      {"name": "Broth", "quantity": "1 cup"},
    ]
  },
  {
    "name": "Tacos",
    "ingredients": [
      {"name": "Tortillas", "quantity": "2"},
      {"name": "Fake Meat", "quantity": "1 cup"},
      {"name": "Onion", "quantity": "1"},
      {"name": "Cilantro", "quantity": "1 bushel"},
    ]
  },
  {
    "name": "Mac and Cheese",
    "ingredients": [
      {"name": "Macaroni", "quantity": "1 box"},
      {"name": "Cheese", "quantity": "1 cup"},
    ]
  },
  {
    "name": "Fried Rice",
    "ingredients": [
      {"name": "Rice", "quantity": "1 cup"},
      {"name": "Oil", "quantity": "2 tbsp"},
      {"name": "Egg", "quantity": "1 egg"},
    ]
  },
  {
    "name": "Omelette",
    "ingredients": [
      {"name": "Egg", "quantity": "2"},
      {"name": "Spinach", "quantity": "1 cup"},
      {"name": "Feta", "quantity": "2 tbsp"},
    ]
  }
]


class Command(BaseCommand):
  help = "Seeds a handful of simple recipes for local dev, skipping any that already exist."

  def handle(self, *args, **options):
    if options["reset"]:
      Ingredient.objects.all().delete()
      Recipe.objects.all().delete()
    created = 0
    for recipe_data in RECIPES:
      recipe_obj, was_created = Recipe.objects.get_or_create(name=recipe_data["name"])
      for ingredient in recipe_data["ingredients"]:
        Ingredient.objects.get_or_create(name=ingredient["name"], quantity=ingredient["quantity"], recipe=recipe_obj)
      created += was_created

    self.stdout.write(self.style.SUCCESS(f"Created {created} recipe(s), skipped {len(RECIPES) - created} existing."))

  def add_arguments(self, parser):
    parser.add_argument(
      "--reset",
      action="store_true",
      help="Delete all existing recipes and ingredients before seeding."
    )
