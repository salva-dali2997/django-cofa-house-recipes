from django.test import TestCase, SimpleTestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe, Ingredient, RecipeIngredient
from .forms import IngredientForm

# Override static file generation dependency for tests
@override_settings(STORAGES={
  "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
  "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class RecipeCreateTest(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(
      username="testuser", 
      email="test@example.com", 
      password="securepassword123"
    )

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
    self.client.force_login(self.user)
    response = self.client.post(reverse("recipes:create"), data)
    self.assertEqual(Recipe.objects.count(), 1)
    recipe = Recipe.objects.get(name="Salad")
    self.assertEqual(recipe.ingredients.count(), 2)
    self.assertRedirects(response, reverse("recipes:view_all"))

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
    self.client.force_login(self.user)
    response = self.client.post(reverse("recipes:create"), data)
    self.assertEqual(Recipe.objects.count(), 0)
    self.assertEqual(response.status_code, 200)

  def test_get_recipes_renders_empty_form(self):
    self.client.force_login(self.user)
    response = self.client.get(reverse("recipes:create"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'id="root"')
    self.assertContains(response, 'id="recipe"')
    self.assertContains(response, 'id="ingredients"')

# Override static file generation dependency for tests
@override_settings(STORAGES={
  "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
  "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class RecipesViewTest(TestCase):
  def setUp(self):
    self.recipe = Recipe.objects.create(name="Cucumber Salad")
    cucumber, _ = Ingredient.objects.get_or_create(name="Cucmber")
    RecipeIngredient.objects.get_or_create(recipe=self.recipe, ingredient=cucumber, quantity="1")
    vinegar, _ = Ingredient.objects.get_or_create(name="Vinegar")
    RecipeIngredient.objects.get_or_create(recipe=self.recipe, ingredient=vinegar, quantity="1/2 Cup")

  def test_200_on_valid_recipes_view(self):
    response = self.client.get(reverse("recipes:view", kwargs={"id": self.recipe.id}))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Cucumber Salad")
    self.assertContains(response, "vinegar")

  def test_404_on_invalid_recipes_view(self):
    response = self.client.get(reverse("recipes:view", kwargs={"id": self.recipe.id + 1}))
    self.assertEqual(response.status_code, 404)

# Uses SimpleTestCase because nothing
# is being written to the database
class IngredientFormTest(SimpleTestCase):
  def test_blank_name_is_invalid(self):
    form = IngredientForm(data={"name": "", "quantity": "1 cup"})
    self.assertFalse(form.is_valid())
    self.assertIn("name", form.errors)

  def test_valid_data_is_valid(self):
    form = IngredientForm(data={"name": "Flour", "quantity": "1 cup"})
    self.assertTrue(form.is_valid())