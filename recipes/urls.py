from django.urls import path
from .views import RecipesViewAll, RecipesCreate, RecipesView, CommentsCreate

app_name = "recipes"

urlpatterns = [
    path("", RecipesViewAll.as_view(), name="view_all"),
    path("create", RecipesCreate.as_view(), name="create"),
    path("<int:id>", RecipesView.as_view(), name="view"),
    path("comment", CommentsCreate.as_view(), name="comment"),
]