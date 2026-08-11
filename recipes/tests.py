from django.test import TestCase
from django.urls import reverse
from .models import Recipe, Ingredient
from .forms import IngredientForm

class RecipeCreateTest(TestCase):
  def test_valid_post_creates_recipes_and_ingredients(self):
    data = {
      "name": "Salad",
      "ingredients-TOTAL_FORMS": "2",
      "ingredients-INITIAL_FORMS": "0",
      "ingredients-MIN_NUM_FORMS": "0",
      "ingredients-MAX_NUM_FORMS": "1000",
      "ingredients-0-name": "Lettuce",
      "ingredients-0-quantity": "8 oz",
      "ingredients-1-name": "Dressing",
      "ingredients-1-quantity": "2 tbsp",
    }
    response = self.client.post(reverse("recipes_create"), data)
    self.assertEqual(Recipe.objects.count(), 1)
    recipe = Recipe.objects.get(name="Salad")
    self.assertEqual(recipe.ingredients.count(), 2)
    self.assertRedirects(response, reverse("recipes_view_all"))

  def test_invalid_post_does_not_create_recipe_or_ingredients(self):
    data = {
      "name": "Salad",
      "ingredients-TOTAL_FORMS": "2",
      "ingredients-INITIAL_FORMS": "0",
      "ingredients-MIN_NUM_FORMS": "0",
      "ingredients-MAX_NUM_FORMS": "1000",
      "ingredients-0-name": "",
      "ingredients-0-quantity": "8 oz",
      "ingredients-1-name": "Dressing",
      "ingredients-1-quantity": "2 tbsp",
    }
    response = self.client.post(reverse("recipes_create"), data)
    self.assertEqual(Recipe.objects.count(), 0)
    self.assertContains(response, '<h1>Create a Recipe</h1>')
    self.assertFormSetError(
      response.context["ingredient_formset"],
      0,
      "name",
      ["This field is required."]
    )

  def test_get_recipes_renders_empty_form(self):
    response = self.client.get(reverse("recipes_create"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, '<h1>Create a Recipe</h1>')