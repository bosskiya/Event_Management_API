from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        ORGANIZER = "organizer", "Organizer"
        ATTENDEE = "attendee", "Attendee"

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.ATTENDEE)

    def is_organizer(self):
        return self.role == self.Roles.ORGANIZER