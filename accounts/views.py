from django.contrib.auth import views
from django.shortcuts import render, redirect
from django.middleware.csrf import get_token
from django.contrib.auth.forms import UserCreationForm
from .models import Invite
from django.contrib.auth import login 
from django.views import View

SIGNUP_ERROR = "This invite code is invalid or has already been used"

def _create_context(request, username="", password1="", password2="", code="", error=""):
    return {
        "csrf_token": get_token(request),
        "username":  username,
        "password1": password1,
        "password2": password2,
        "code": code,
        "error": error
    }

class LoginView(views.LoginView):
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["csrf_token"] = get_token(self.request)
    return context

class LogoutConfirmView(View):
  def get(self, request):
    return render(request, "registration/logout_confirm.html")

class SignupView(View):
  def get(self, request, code):
    return render(request, "registration/signup.html", _create_context(request, code=code))

  def post(self, request, code):
    invite = Invite.objects.filter(id=code, used_by__isnull=True).first()
    if invite is None:
      return render(request, "registration/signup.html", _create_context(request, code=code, error=SIGNUP_ERROR))
    signup_form = UserCreationForm(request.POST)
    if not signup_form.is_valid():
      context = _create_context(
        request, 
        request.POST.get("username", ""),
        request.POST.get("password1", ""),
        request.POST.get("password2", ""),
        code,
        error=signup_form.errors.as_text()
      )
      return render(request, "registration/signup.html", context)
    user = signup_form.save()
    login(request, user)
    invite.used_by = user
    invite.save()
    return redirect("recipes:view_all")