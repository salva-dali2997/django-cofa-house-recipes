from django.urls import path
from .views import RecipesViewAll, RecipesCreate, RecipesView, CommentsCreate

app_name = "recipes"

urlpatterns = [
    path("", RecipesViewAll.as_view(), name="view_all"),
    path("create", RecipesCreate.as_view(), name="create"),
    path("today", RecipesToday.as_view(), name="today"),
    path("today/manage", MenuManage.as_view(), name="today_manage"),
    path("today/toggle", MenuRecipeToggle.as_view(), name="today_toggle"),
    path("<int:id>", RecipesView.as_view(), name="view"),
    path("comment", CommentsCreate.as_view(), name="comment"),
]