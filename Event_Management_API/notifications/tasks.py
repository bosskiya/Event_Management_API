from celery import shared_task
from .services import send_registration_email, send_reminder_email


@shared_task
def send_registration_confirmation(user_email: str, event_title: str):
    send_registration_email(user_email, event_title)


@shared_task
def send_event_reminder(user_email: str, event_title: str):
    send_reminder_email(user_email, event_title)