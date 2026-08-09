from django import forms

class RecipeForm(forms.Form):
  name = forms.CharField(label="Recipe Name", max_length=40)

class IngredientsForm(forms.Form):
  name = forms.CharField(max_length=20)
  quantity = forms.CharField(max_length=10)