from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Recipe
from .forms import RecipeForm, IngredientFormSet
from django.db import transaction

class RecipesViewAll(View):
  def get(self, request):
    last_ten_recipes = Recipe.objects.order_by('-created_at')[:10]
    recipes_data = list(last_ten_recipes.values('id', 'name'))
    context = {"recipes_data": recipes_data}
    return render(request, "recipes/recipes_view_all.html", context)

class RecipesCreate(View):
  def get(self, request):
    recipe_form = RecipeForm()
    ingredient_formset = IngredientFormSet()
    return render(request, "recipes/recipes_create.html", 
                    {
                      "recipe_form": recipe_form,
                      "ingredient_formset": ingredient_formset
                    })
  
  def post(self, request):
    recipe_form = RecipeForm(request.POST)
    ingredient_formset = IngredientFormSet(request.POST, instance=recipe_form.instance)
    if not (recipe_form.is_valid() and ingredient_formset.is_valid()):
      return render(request, "recipes/recipes_create.html", {
          "recipe_form": recipe_form,
          "ingredient_formset": ingredient_formset
        })
    with transaction.atomic():
      recipe_form.save()
      ingredient_formset.save()
    return redirect("recipes_view_all")

class RecipesView(View):
  def get(self, request, id):
    recipe = get_object_or_404(Recipe, id=id)
    # ingredients = Book.objects.select_related('author', 'publisher').filter(is_published=True)
    ingredients = recipe.ingredients.all()
    return render(request, 'recipes/recipes_view.html', {
      'recipe': recipe,
      'ingredients': ingredients,
    })