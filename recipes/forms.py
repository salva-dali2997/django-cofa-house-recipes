from django import forms
from .models import Recipe, Ingredient, RecipeIngredient
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

class RecipeForm(forms.ModelForm):
  class Meta:
    model = Recipe
    fields = ['name']

class IngredientForm(forms.ModelForm):
  class Meta:
    model = RecipeIngredient
    fields = ['quantity']
    
  name = forms.CharField(label=_("Ingredient"))

  def save(self, commit=True):
    instance = super().save(commit=False)
    instance.ingredient, _ = Ingredient.objects.get_or_create(name=self.cleaned_data['name'])
    if commit:
      instance.save()
    return instance

  def clean_name(self):
    raw_data = self.cleaned_data.get('name')
    return Ingredient.normalize(raw_data)

IngredientFormSet = inlineformset_factory(
  Recipe,
  RecipeIngredient,
  form=IngredientForm,
  extra=3,
  can_delete=False,
  min_num=1,
  validate_min=True
)