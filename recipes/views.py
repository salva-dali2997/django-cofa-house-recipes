from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from .models import Recipe, Ingredient, Comment
from .forms import RecipeForm, IngredientFormSet
from django.db import transaction
from django.middleware.csrf import get_token
from django.contrib.auth.mixins import LoginRequiredMixin

def _ingredients_from_post(post_data):
  total_forms = int(post_data.get("ingredients-TOTAL_FORMS", 0))
  if not total_forms:
    return [{"name": "", "quantity": ""}]
  return [
    {
      "name": post_data.get(f"ingredients-{i}-name", ""),
      "quantity": post_data.get(f"ingredients-{i}-quantity", ""),
    }
    for i in range(total_forms)
  ]

def _create_context(request, recipe_name="", ingredients=None, suggestions=None):
    return {
        "csrf_token": get_token(request),
        "recipe": {"name": recipe_name},
        "ingredients": ingredients or [{"name": "", "quantity": ""}],
        "suggestions": suggestions or []
    }

def _ingredient_create_confirmation(ingredient_name, confirm_create): 
  if confirm_create:
    return None
  matches = Ingredient.check_existing_ingredients(ingredient_name)
  if not matches or matches[0] == ingredient_name:
    return None
  return matches[0]

class RecipesViewAll(View):
  def get(self, request):
    all_recipes = Recipe.objects.order_by('-created_at')
    paginator = Paginator(all_recipes, RECIPES_PER_PAGE)
    page = paginator.get_page(request.GET.get('page'))
    recipes_data = list(page.object_list.values('id', 'name'))
    context = {
      "recipes_data": recipes_data,
      "pagination": {
        "current_page": page.number,
        "total_pages": paginator.num_pages,
        "has_previous": page.has_previous(),
        "has_next": page.has_next(),
        "previous_page": page.previous_page_number() if page.has_previous() else None,
        "next_page": page.next_page_number() if page.has_next() else None,
      },
    }
    return render(request, "recipes/view_all.html", context)

class RecipesCreate(LoginRequiredMixin, View):
  def get(self, request):
    return render(request, "recipes/create.html", _create_context(request))
  
  def post(self, request):
    recipe_form = RecipeForm(request.POST)
    ingredient_formset = IngredientFormSet(request.POST, instance=recipe_form.instance)
    if not (recipe_form.is_valid() and ingredient_formset.is_valid()):
      context = _create_context(
        request, 
        request.POST.get("name", ""),
        _ingredients_from_post(request.POST)
      )
      return render(request, "recipes/create.html", context)
    suggestions = [
      (i, s)
      for i, form in enumerate(ingredient_formset.forms)
      if (s := _ingredient_create_confirmation(
        form.cleaned_data['name'], 
        request.POST.get(f"ingredients-{i}-confirmed")
      ))
    ]
    if suggestions:
      context = _create_context(
        request, 
        request.POST.get("name", ""),
        _ingredients_from_post(request.POST),
        suggestions
      )
      return render(request, "recipes/create.html", context)
    with transaction.atomic():
      recipe_form.save()
      ingredient_formset.save()
    return redirect("recipes:view_all")

class RecipesView(View):
  def get(self, request, id):
    recipe = get_object_or_404(Recipe, id=id)
    ingredients = recipe.ingredients.all()
    comments = recipe.comments.all()
    context = {
      "recipe": {"id": recipe.id, "name": recipe.name},
      "ingredients": list(ingredients.values("quantity", "ingredient__name")),
      "comments": list(comments.values("content")),
      "csrf_token": get_token(request)
    }
    return render(request, 'recipes/view.html', context)

class CommentsCreate(View):
  def post(self, request):
    recipe = get_object_or_404(Recipe, id=request.POST.get("recipe_id"))
    content = request.POST.get("comment", "").strip()
    if not content:
      return JsonResponse({"error": "Comment cannot be empty"}, status=400)
    comment = Comment.objects.create(recipe=recipe, content=content)
    return JsonResponse({"content": comment.content, "created_at": comment.created_at.isoformat()})

class RecipesToday(View):
  """Public page: shows only the recipes currently on the menu. No login required."""
  def get(self, request):
    menu = _get_menu()
    recipes_data = list(menu.recipe_set.order_by('name').values('id', 'name'))
    context = {"recipes_data": recipes_data}
    return render(request, "recipes/today.html", context)

class MenuManage(LoginRequiredMixin, View):
  """Admin-only page for choosing which recipes are on today's menu."""
  def get(self, request):
    if not request.user.is_superuser:
      return redirect("recipes:today")
    menu = _get_menu()
    on_menu_ids = set(menu.recipe_set.values_list('id', flat=True))
    recipes_data = [
      {"id": recipe.id, "name": recipe.name, "on_menu": recipe.id in on_menu_ids}
      for recipe in Recipe.objects.order_by('name')
    ]
    context = {
      "recipes_data": recipes_data,
      "csrf_token": get_token(request),
    }
    return render(request, "recipes/today_manage.html", context)

class MenuRecipeToggle(View):
  def post(self, request):
    if not request.user.is_superuser:
      return JsonResponse({"error": "Forbidden"}, status=403)
    menu = _get_menu()
    recipe = get_object_or_404(Recipe, id=request.POST.get("recipe_id"))
    if menu.recipe_set.filter(id=recipe.id).exists():
      menu.recipe_set.remove(recipe)
      on_menu = False
    else:
      menu.recipe_set.add(recipe)
      on_menu = True
    return JsonResponse({"id": recipe.id, "on_menu": on_menu})