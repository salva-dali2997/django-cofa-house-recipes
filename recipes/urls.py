from django.urls import path
from .views import RecipesView, RecipesCreate

urlpatterns = [
    path("", RecipesView.as_view(), name="recipes_view"),
    path("/create", RecipesCreate.as_view(), name="recipes_create"),
]