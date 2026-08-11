from django.urls import path
from .views import RecipesViewAll, RecipesCreate, RecipesView

urlpatterns = [
    path("", RecipesViewAll.as_view(), name="recipes_view_all"),
    path("create", RecipesCreate.as_view(), name="recipes_create"),
    path("<int:id>", RecipesView.as_view(), name="recipes_view"),
]