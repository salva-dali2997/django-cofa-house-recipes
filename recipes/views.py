from django.shortcuts import render
from django.views import View
from .models import Recipe

class RecipesView(View):
    def get(self, request):
        last_ten_recipes = Recipe.objects.order_by('-created_at')[:10]
        recipes_data = list(last_ten_recipes.values('id', 'name'))
        context = {"recipes_data": recipes_data}
        return render(request, "recipes/recipes_view.html", context)