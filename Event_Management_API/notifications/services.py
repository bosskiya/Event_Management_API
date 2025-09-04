from django.core.mail import send_mail
from django.conf import settings


def send_registration_email(user_email: str, event_title: str):
    send_mail(
        subject=f"Registration confirmed: {event_title}",
        message=f"You have successfully registered for {event_title}.",
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com"),
        recipient_list=[user_email],
        fail_silently=True,
    )


def send_reminder_email(user_email: str, event_title: str):
    send_mail(
        subject=f"Reminder: {event_title} is coming soon",
        message=f"Don't forget! {event_title} is starting soon.",
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com"),
        recipient_list=[user_email],
        fail_silently=True,
    )