from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.timezone import now

# Create your models here.
class Invite(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  used_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
  created_at = models.DateTimeField(default=now)