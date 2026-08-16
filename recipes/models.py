from django.db import models
from difflib import get_close_matches

class Menu(models.Model):
  date = models.DateField()

class Recipe(models.Model):
  name = models.CharField(max_length=40)
  created_at = models.DateTimeField(auto_now_add=True)
  menu = models.ManyToManyField(Menu, null=True)

class Ingredient(models.Model):
  name = models.CharField(max_length=20, unique=True)

  def save(self, *args, **kwargs):
    self.name = Ingredient.normalize(self.name)
    super().save(*args, **kwargs)

  @staticmethod
  def normalize(ingredient_name):
    return ingredient_name.strip().lower()

  @staticmethod
  def check_existing_ingredients(ingredient_name):
    return get_close_matches(
      ingredient_name, 
      list(Ingredient.objects.values_list('name', flat=True))
    )


class RecipeIngredient(models.Model):
  quantity = models.CharField(max_length=10)
  ingredient = models.ForeignKey(
    Ingredient, 
    on_delete=models.PROTECT, 
    related_name='recipe_uses'
  )
  recipe = models.ForeignKey(
    Recipe, 
    on_delete=models.CASCADE, 
    related_name='ingredients'
  )

class Comment(models.Model):
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)