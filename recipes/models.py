from django.db import models

# Create your models here.
class Recipe(models.Model):
  name = models.CharField(max_length=40)
  created_at = models.DateTimeField(auto_now_add=True)