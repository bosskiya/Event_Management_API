from django.urls import path
from .views import MyRegistrationsView, RegisterForEventView

urlpatterns = [
    path("me/", MyRegistrationsView.as_view(), name="my-registrations"),
    path("register/", RegisterForEventView.as_view(), name="event-register"),
]