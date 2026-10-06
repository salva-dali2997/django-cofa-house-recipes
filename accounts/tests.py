from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Invite


@override_settings(STORAGES={
  "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
  "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class LoginViewTest(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(username="someone", password="correct-password")

  def test_get_renders_login_form(self):
    response = self.client.get("/accounts/login")
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'id="csrf_token"')

  def test_correct_credentials_log_in_and_redirect(self):
    response = self.client.post("/accounts/login", {
      "username": "someone",
      "password": "correct-password",
    })
    self.assertRedirects(response, "/recipes/")
    self.assertIn("_auth_user_id", self.client.session)

  def test_wrong_password_does_not_log_in(self):
    response = self.client.post("/accounts/login", {
      "username": "someone",
      "password": "wrong-password",
    })
    self.assertEqual(response.status_code, 200)
    self.assertFalse(response.context["user"].is_authenticated)


@override_settings(STORAGES={
  "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
  "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class SignupViewTest(TestCase):
  def setUp(self):
    self.invite = Invite.objects.create()

  def test_get_renders_signup_form(self):
    response = self.client.get(f"/accounts/signup/{self.invite.id}")
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'id="csrf_token"')

  def test_invalid_invite_code_shows_error(self):
    response = self.client.post("/accounts/signup/00000000-0000-0000-0000-000000000000", {
      "username": "newperson",
      "password1": "a-very-strong-pw-123",
      "password2": "a-very-strong-pw-123",
    })
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "invalid or has already been used")
    self.assertFalse(User.objects.filter(username="newperson").exists())

  def test_valid_invite_creates_user_and_logs_in(self):
    response = self.client.post(f"/accounts/signup/{self.invite.id}", {
      "username": "newperson",
      "password1": "a-very-strong-pw-123",
      "password2": "a-very-strong-pw-123",
    })
    self.assertRedirects(response, reverse("recipes:view_all"))
    user = User.objects.get(username="newperson")
    self.invite.refresh_from_db()
    self.assertEqual(self.invite.used_by, user)

  def test_already_used_invite_is_rejected(self):
    used_by = User.objects.create_user(username="firstperson", password="pw")
    self.invite.used_by = used_by
    self.invite.save()

    response = self.client.post(f"/accounts/signup/{self.invite.id}", {
      "username": "secondperson",
      "password1": "a-very-strong-pw-123",
      "password2": "a-very-strong-pw-123",
    })
    self.assertContains(response, "invalid or has already been used")
    self.assertFalse(User.objects.filter(username="secondperson").exists())

  def test_mismatched_passwords_rerenders_with_error(self):
    response = self.client.post(f"/accounts/signup/{self.invite.id}", {
      "username": "newperson",
      "password1": "a-very-strong-pw-123",
      "password2": "does-not-match",
    })
    self.assertEqual(response.status_code, 200)
    self.assertFalse(User.objects.filter(username="newperson").exists())


@override_settings(STORAGES={
  "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
  "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class LogoutConfirmViewTest(TestCase):
  def test_get_renders_confirm_page(self):
    response = self.client.get("/accounts/logout-confirm")
    self.assertEqual(response.status_code, 200)
