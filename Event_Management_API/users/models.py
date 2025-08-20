from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_organizer = models.BooleanField(default=False)
    is_attendee = models.BooleanField(default=True)
