from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from registrations.models import Registration
from notifications.tasks import send_registration_confirmation, send_event_reminder


@receiver(post_save, sender=Registration)
def handle_registration_created(sender, instance: Registration, created, **kwargs):
    if not created:
        return

    # Send confirmation immediately
    send_registration_confirmation.delay(instance.user.email, instance.event.title)

    # Schedule reminder 3 hours before event start
    eta = instance.event.date_time - timedelta(hours=3)
    if eta > timezone.now():
        send_event_reminder.apply_async(
            args=[instance.user.email, instance.event.title],
            eta=eta,
        )