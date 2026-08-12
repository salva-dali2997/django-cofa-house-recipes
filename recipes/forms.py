from django import forms
from .models import Recipe, Ingredient
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

class RecipeForm(forms.ModelForm):
  class Meta:
    model = Recipe
    fields = ['name']

class IngredientForm(forms.ModelForm):
  class Meta:
    model = Ingredient
    fields = ['name', 'quantity']
    labels = {"name": _("Ingredient")}

IngredientFormSet = inlineformset_factory(
  Recipe,
  Ingredient,
  form=IngredientForm,
  extra=3,
  can_delete=False,
  min_num=1,
  validate_min=True
)