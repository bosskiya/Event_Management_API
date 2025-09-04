from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import Registration
from ticket.models import Ticket
from notifications.tasks import send_registration_confirmation, send_event_reminder


@receiver(post_save, sender=Registration)
def handle_registration_created(sender, instance: Registration, created, **kwargs):
    """Send confirmation immediately + reminder before event."""
    if not created:
        return

    # Create ticket if not waitlisted
    if not instance.is_waitlisted:
        Ticket.objects.create(registration=instance)

    # Send confirmation email right away
    send_registration_confirmation.delay(instance.user.email, instance.event.title)

    # Schedule reminder email 3 hours before event
    eta = instance.event.date_time - timedelta(hours=3)
    if eta > timezone.now():
        send_event_reminder.apply_async(
            args=[instance.user.email, instance.event.title],
            eta=eta,
        )