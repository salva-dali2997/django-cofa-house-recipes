from django.core.management.base import BaseCommand

from recipes.models import Recipe

RECIPE_NAMES = [
    "Pancakes",
    "Spaghetti",
    "Grilled Cheese",
    "Caesar Salad",
    "Tomato Soup",
    "Curry",
    "Tacos",
    "Stir Fry",
    "Banana Bread",
    "Mac and Cheese",
    "Fried Rice",
    "Omelette",
    "Chili",
    "Pizza",
    "Lasagna",
]


class Command(BaseCommand):
    help = "Seeds a handful of simple recipes for local dev, skipping any that already exist."

    def handle(self, *args, **options):
        created = 0
        for name in RECIPE_NAMES:
            _, was_created = Recipe.objects.get_or_create(name=name)
            created += was_created

        self.stdout.write(self.style.SUCCESS(f"Created {created} recipe(s), skipped {len(RECIPE_NAMES) - created} existing."))
