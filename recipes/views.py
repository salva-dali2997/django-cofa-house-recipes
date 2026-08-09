from django.shortcuts import render, redirect
from django.views import View
from .models import Recipe
from .forms import RecipeForm, IngredientsForm
from django.forms import formset_factory

class RecipesView(View):
  def get(self, request):
    last_ten_recipes = Recipe.objects.order_by('-created_at')[:10]
    recipes_data = list(last_ten_recipes.values('id', 'name'))
    context = {"recipes_data": recipes_data}
    return render(request, "recipes/recipes_view.html", context)

class RecipesCreate(View):
  def get(self, request):
    recipe_form = RecipeForm()
    ingredients_formset = formset_factory(IngredientsForm, max_num=25)
    return render(request, "recipes/recipes_create.html", 
                    {
                      "recipe_form": recipe_form,
                      "ingredients_form": ingredients_formset
                    })
  def post(self, request):
    recipe_form = RecipeForm(request.POST)
    if recipe_form.is_valid():
        print(request.POST)
    else:
        print(request.POST)
    return redirect("recipes/recipes_view.html")