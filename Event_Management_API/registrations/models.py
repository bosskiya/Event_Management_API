from django.db import models
from users.models import User
from events.models import Event

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    is_waitlisted = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'event']
