from django.db import models
from django.conf import settings
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    class Visibility(models.TextChoices):
        PUBLIC = "public", "Public"
        PRIVATE = "private", "Private"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organized_events")
    visibility = models.CharField(max_length=10, choices=Visibility.choices, default=Visibility.PUBLIC)
    image = models.ImageField(upload_to="event_images/", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["date_time"]
        indexes = [models.Index(fields=["date_time"]) ]

    def __str__(self):
        return self.title

    @property
    def is_past(self):
        return self.date_time <= timezone.now()

class Speaker(models.Model):
    name = models.CharField(max_length=120)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Session(models.Model):
    event = models.ForeignKey(Event, related_name="sessions", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    speaker = models.ForeignKey(Speaker, related_name="sessions", on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        ordering = ["start_time"]

class TicketType(models.Model):
    event = models.ForeignKey(Event, related_name="ticket_types", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)   # e.g., General, VIP
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ("event", "name")

    def __str__(self):
        return f"{self.event.title} — {self.name}"