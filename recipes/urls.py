from django.urls import path
from .views import RecipesView

urlpatterns = [
    path("", RecipesView.as_view(), name="recipes_view"),
]