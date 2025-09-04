from django.db import models
from django.conf import settings
from django.utils import timezone
from events.models import Event, TicketType


class Registration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="registrations", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="registrations", on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, related_name="registrations", on_delete=models.SET_NULL, null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    is_waitlisted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "event")

    def save(self, *args, **kwargs):
        if not self.pk:  # only on creation
            current_count = Registration.objects.filter(event=self.event, is_waitlisted=False).count()
            if self.event.capacity and current_count >= self.event.capacity:
                self.is_waitlisted = True
        super().save(*args, **kwargs)

    def __str__(self):
        status = "Waitlisted" if self.is_waitlisted else "Confirmed"
        return f"{self.user.username} -> {self.event.title} ({status})"