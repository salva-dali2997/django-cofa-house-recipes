from django.urls import path
from .views import LoginView, SignupView, LogoutConfirmView
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path("login", LoginView.as_view()),
    path("signup/<uuid:code>", SignupView.as_view()),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    path("logout-confirm", LogoutConfirmView.as_view()),
]