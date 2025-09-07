from django.urls import path
from .views import MyRegistrationsView, RegisterForEventView, register_for_event, check_in_ticket

urlpatterns = [
    path("me/", MyRegistrationsView.as_view(), name="my-registrations"),
    path("register/", RegisterForEventView.as_view(), name="event-register"),
    path("<int:event_id>/register/", register_for_event, name="event-register"),
    path("ticket/<uuid:code>/checkin/", check_in_ticket, name="ticket-checkin"),
]