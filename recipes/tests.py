import io
import sqlite3
import tempfile
from pathlib import Path

from django.test import TestCase, SimpleTestCase, override_settings
from django.urls import reverse
from django.core.management import call_command
from django.contrib.auth.models import User
from .models import Recipe, Ingredient, RecipeIngredient, Comment, Menu
from .forms import IngredientForm, RecipeForm

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

  def test_close_match_ingredient_name_suggests_existing_one(self):
    Ingredient.objects.create(name="lettuce")
    data = {
      "name": "Salad",
      "ingredients-TOTAL_FORMS": "1",
      "ingredients-INITIAL_FORMS": "0",
      "ingredients-MIN_NUM_FORMS": "0",
      "ingredients-MAX_NUM_FORMS": "1000",
      "ingredients-0-name": "letuce",
      "ingredients-0-quantity": "8 oz",
    }
    self.client.force_login(self.user)
    response = self.client.post(reverse("recipes:create"), data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Recipe.objects.count(), 0)
    self.assertContains(response, "lettuce")

  def test_confirmed_close_match_ingredient_name_is_accepted(self):
    Ingredient.objects.create(name="lettuce")
    data = {
      "name": "Salad",
      "ingredients-TOTAL_FORMS": "1",
      "ingredients-INITIAL_FORMS": "0",
      "ingredients-MIN_NUM_FORMS": "0",
      "ingredients-MAX_NUM_FORMS": "1000",
      "ingredients-0-name": "letuce",
      "ingredients-0-quantity": "8 oz",
      "ingredients-0-confirmed": "true",
    }
    self.client.force_login(self.user)
    response = self.client.post(reverse("recipes:create"), data)
    self.assertRedirects(response, reverse("recipes:view_all"))
    self.assertEqual(Recipe.objects.count(), 1)

  def test_missing_formset_management_data_rerenders_with_blank_ingredient(self):
    self.client.force_login(self.user)
    response = self.client.post(reverse("recipes:create"), {"name": "Salad"})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Recipe.objects.count(), 0)

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


class RecipeFormTest(SimpleTestCase):
  def test_directions_is_optional(self):
    form = RecipeForm(data={"name": "Salad"})
    self.assertTrue(form.is_valid())

  def test_directions_is_saved(self):
    form = RecipeForm(data={"name": "Salad", "directions": "1. Chop.\n2. Toss."})
    self.assertTrue(form.is_valid())
    self.assertEqual(form.cleaned_data["directions"], "1. Chop.\n2. Toss.")


class IngredientModelTest(TestCase):
  def test_normalize_strips_and_lowercases(self):
    self.assertEqual(Ingredient.normalize("  Kosher Salt  "), "kosher salt")

  def test_save_normalizes_name(self):
    ingredient = Ingredient.objects.create(name="  Tomato ")
    self.assertEqual(ingredient.name, "tomato")

  def test_check_existing_ingredients_finds_close_match(self):
    Ingredient.objects.create(name="cilantro")
    matches = Ingredient.check_existing_ingredients("cilantro")
    self.assertIn("cilantro", matches)

  def test_check_existing_ingredients_no_match(self):
    Ingredient.objects.create(name="cilantro")
    matches = Ingredient.check_existing_ingredients("xyzzyplugh")
    self.assertEqual(matches, [])


class RootRedirectTest(TestCase):
  def test_root_redirects_to_recipes(self):
    response = self.client.get("/")
    self.assertRedirects(response, "/recipes/", status_code=302, fetch_redirect_response=False)


@override_settings(STORAGES={
  "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
  "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class RecipesViewAllPaginationTest(TestCase):
  def setUp(self):
    for i in range(15):
      Recipe.objects.create(name=f"Recipe {i:02d}")

  def test_first_page_has_ten_and_next_page(self):
    response = self.client.get(reverse("recipes:view_all"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, '"total_pages": 2')
    self.assertContains(response, '"has_next": true')
    self.assertContains(response, '"has_previous": false')

  def test_second_page_has_remaining_five(self):
    response = self.client.get(reverse("recipes:view_all"), {"page": 2})
    self.assertContains(response, '"current_page": 2')
    self.assertContains(response, '"has_next": false')
    self.assertContains(response, '"has_previous": true')

  def test_out_of_range_page_clamps_to_last_page(self):
    response = self.client.get(reverse("recipes:view_all"), {"page": 99})
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, '"current_page": 2')


@override_settings(STORAGES={
  "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
  "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class CommentsCreateTest(TestCase):
  def setUp(self):
    self.recipe = Recipe.objects.create(name="Cucumber Salad")

  def test_valid_comment_is_created(self):
    response = self.client.post(reverse("recipes:comment"), {
      "recipe_id": self.recipe.id,
      "comment": "So good!",
    })
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Comment.objects.count(), 1)
    comment = Comment.objects.get()
    self.assertEqual(comment.content, "So good!")
    self.assertEqual(comment.recipe, self.recipe)

  def test_empty_comment_is_rejected(self):
    response = self.client.post(reverse("recipes:comment"), {
      "recipe_id": self.recipe.id,
      "comment": "   ",
    })
    self.assertEqual(response.status_code, 400)
    self.assertEqual(Comment.objects.count(), 0)

  def test_comment_on_missing_recipe_404s(self):
    response = self.client.post(reverse("recipes:comment"), {
      "recipe_id": self.recipe.id + 1,
      "comment": "Hi",
    })
    self.assertEqual(response.status_code, 404)


@override_settings(STORAGES={
  "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
  "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class RecipesTodayTest(TestCase):
  def setUp(self):
    self.on_menu = Recipe.objects.create(name="On The Menu")
    self.off_menu = Recipe.objects.create(name="Not On The Menu")
    self.menu = Menu.objects.create(date="2026-01-01")
    self.menu.recipe_set.add(self.on_menu)

  def test_public_page_shows_only_on_menu_recipes_no_login_required(self):
    response = self.client.get(reverse("recipes:today"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "On The Menu")
    self.assertNotContains(response, "Not On The Menu")


@override_settings(STORAGES={
  "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
  "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class MenuManageTest(TestCase):
  def setUp(self):
    self.admin = User.objects.create_superuser(username="admin", email="a@a.com", password="pw")
    self.regular_user = User.objects.create_user(username="regular", password="pw")
    self.recipe = Recipe.objects.create(name="Some Recipe")

  def test_anonymous_user_redirected_to_login(self):
    response = self.client.get(reverse("recipes:today_manage"))
    self.assertEqual(response.status_code, 302)
    self.assertIn("/accounts/login", response.url)

  def test_non_superuser_redirected_to_today(self):
    self.client.force_login(self.regular_user)
    response = self.client.get(reverse("recipes:today_manage"))
    self.assertRedirects(response, reverse("recipes:today"))

  def test_superuser_sees_all_recipes_with_on_menu_flag(self):
    self.client.force_login(self.admin)
    response = self.client.get(reverse("recipes:today_manage"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Some Recipe")


@override_settings(STORAGES={
  "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
  "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class MenuRecipeToggleTest(TestCase):
  def setUp(self):
    self.admin = User.objects.create_superuser(username="admin", email="a@a.com", password="pw")
    self.regular_user = User.objects.create_user(username="regular", password="pw")
    self.recipe = Recipe.objects.create(name="Some Recipe")

  def test_non_superuser_forbidden(self):
    self.client.force_login(self.regular_user)
    response = self.client.post(reverse("recipes:today_toggle"), {"recipe_id": self.recipe.id})
    self.assertEqual(response.status_code, 403)

  def test_superuser_can_toggle_recipe_onto_and_off_menu(self):
    self.client.force_login(self.admin)
    url = reverse("recipes:today_toggle")

    response = self.client.post(url, {"recipe_id": self.recipe.id})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), {"id": self.recipe.id, "on_menu": True})

    response = self.client.post(url, {"recipe_id": self.recipe.id})
    self.assertEqual(response.json(), {"id": self.recipe.id, "on_menu": False})


class SeedRecipesCommandTest(TestCase):
  def test_seeds_ten_recipes_and_is_idempotent(self):
    call_command("seed_recipes", stdout=io.StringIO())
    self.assertEqual(Recipe.objects.count(), 10)
    call_command("seed_recipes", stdout=io.StringIO())
    self.assertEqual(Recipe.objects.count(), 10)

  def test_reset_deletes_before_reseeding(self):
    Recipe.objects.create(name="Leftover Junk")
    call_command("seed_recipes", "--reset", stdout=io.StringIO())
    self.assertEqual(Recipe.objects.count(), 10)
    self.assertFalse(Recipe.objects.filter(name="Leftover Junk").exists())


class EnsureSuperuserCommandTest(TestCase):
  def test_creates_superuser_from_env_defaults(self):
    call_command("ensure_superuser", stdout=io.StringIO())
    user = User.objects.get(username="admin")
    self.assertTrue(user.is_superuser)

  def test_skips_if_username_already_exists(self):
    User.objects.create_user(username="admin", password="something")
    call_command("ensure_superuser", stdout=io.StringIO())
    self.assertEqual(User.objects.filter(username="admin").count(), 1)
    self.assertFalse(User.objects.get(username="admin").is_superuser)


class ImportLegacyDataCommandTest(TestCase):
  def setUp(self):
    self.tmpdir = tempfile.TemporaryDirectory()
    self.addCleanup(self.tmpdir.cleanup)
    self.db_path = str(Path(self.tmpdir.name) / "legacy.db")
    self._build_legacy_db(self.db_path)

  def _build_legacy_db(self, path):
    conn = sqlite3.connect(path)
    conn.executescript("""
      CREATE TABLE recipes (id INTEGER PRIMARY KEY, name TEXT, instructions TEXT, created_at TEXT);
      CREATE TABLE ingredients (id INTEGER PRIMARY KEY, name TEXT, quantity TEXT, recipe_id INTEGER);
      CREATE TABLE feedbacks (id INTEGER PRIMARY KEY, name TEXT, comment TEXT, recipe_id INTEGER, created_at TEXT);
      CREATE TABLE menus (id INTEGER PRIMARY KEY, date TEXT);
      CREATE TABLE menu_recipes (id INTEGER PRIMARY KEY, menu_id INTEGER, recipe_id INTEGER);
    """)
    conn.execute(
      "INSERT INTO recipes VALUES (1, 'Legacy Salad', '1. Chop.\n2. Toss.', '2026-01-01 00:00:00.000000')"
    )
    conn.execute("INSERT INTO ingredients VALUES (1, 'Lettuce', '1 head', 1)")
    conn.execute(
      "INSERT INTO feedbacks VALUES (1, 'legacy user', 'delicious', 1, '2026-01-02 00:00:00.000000')"
    )
    conn.execute("INSERT INTO menus VALUES (1, '2026-01-01')")
    conn.execute("INSERT INTO menu_recipes VALUES (1, 1, 1)")
    conn.commit()
    conn.close()

  def test_imports_recipes_ingredients_comments_and_menus(self):
    call_command("import_legacy_data", "--path", self.db_path, stdout=io.StringIO())

    recipe = Recipe.objects.get(name="Legacy Salad")
    self.assertEqual(recipe.directions, "1. Chop.\n2. Toss.")
    self.assertEqual(recipe.ingredients.count(), 1)
    self.assertEqual(recipe.ingredients.get().ingredient.name, "lettuce")

    comment = Comment.objects.get()
    self.assertEqual(comment.content, "legacy user: delicious")
    self.assertEqual(comment.recipe, recipe)

    menu = Menu.objects.get()
    self.assertIn(recipe, menu.recipe_set.all())

  def test_import_is_idempotent(self):
    call_command("import_legacy_data", "--path", self.db_path, stdout=io.StringIO())
    call_command("import_legacy_data", "--path", self.db_path, stdout=io.StringIO())
    self.assertEqual(Recipe.objects.count(), 1)
    self.assertEqual(Comment.objects.count(), 1)
    self.assertEqual(Menu.objects.count(), 1)

  def test_orphaned_ingredient_and_feedback_rows_are_skipped(self):
    conn = sqlite3.connect(self.db_path)
    # recipe_id 999 doesn't exist in the recipes table
    conn.execute("INSERT INTO ingredients VALUES (2, 'Ghost Ingredient', '1', 999)")
    conn.execute(
      "INSERT INTO feedbacks VALUES (2, NULL, 'orphaned comment', 999, '2026-01-01 00:00:00.000000')"
    )
    conn.commit()
    conn.close()

    call_command("import_legacy_data", "--path", self.db_path, stdout=io.StringIO())

    self.assertFalse(Ingredient.objects.filter(name="ghost ingredient").exists())
    self.assertFalse(Comment.objects.filter(content="orphaned comment").exists())