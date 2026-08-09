from django.db import models

class Menu(models.Model):
  date = models.DateField()

class Recipe(models.Model):
  name = models.CharField(max_length=40)
  created_at = models.DateTimeField(auto_now_add=True)
  menu = models.ManyToManyField(Menu, null=True)

class Ingredient(models.Model):
  name = models.CharField(max_length=20)
  quantity = models.CharField(max_length=10)
  recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT, related_name='ingredients')

class Comment(models.Model):
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)