import uuid
from django.db import models
from registrations.models import Registration


class Ticket(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, related_name="ticket")
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    issued_at = models.DateTimeField(auto_now_add=True)
    is_checked_in = models.BooleanField(default=False)

    def __str__(self):
        return f"Ticket {self.code} for {self.registration.event.title}"

    def mark_checked_in(self):
        self.is_checked_in = True
        self.save(update_fields=["is_checked_in"])