from django.db import models
from events.models import Event


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    type = models.CharField(max_length=100)  # e.g., General, VIP
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.PositiveIntegerField()