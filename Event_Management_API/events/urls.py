from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView, CategoryViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)

urlpatterns = [
    path("", EventListView.as_view(), name="event-list"),
    path("<int:pk>/", EventDetailView.as_view(), name="event-detail"),
    path("create/", EventCreateView.as_view(), name="event-create"),
    path("<int:pk>/update/", EventUpdateView.as_view(), name="event-update"),
    path("<int:pk>/delete/", EventDeleteView.as_view(), name="event-delete"),

    # category API
    path("", include(router.urls)),
]