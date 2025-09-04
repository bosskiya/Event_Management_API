from rest_framework import generics, permissions, filters, viewsets, permissions
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event
from .models import Category
from .serializers import EventSerializer, CategorySerializer


class EventListView(generics.ListAPIView):
    """
    List all upcoming events (public).
    Supports search by title/description and filtering by location, category, date range.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["title", "description", "location"]
    filterset_fields = ["location", "category", "organizer"]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(date_time__gte=timezone.now(), visibility="public")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        if start_date and end_date:
            qs = qs.filter(date_time__range=[start_date, end_date])
        return qs.order_by("date_time")


class EventDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single event by ID.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]


class EventCreateView(generics.CreateAPIView):
    """
    Organizers can create events.
    """
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != "organizer":
            raise PermissionError("Only organizers can create events.")
        serializer.save(organizer=self.request.user)


class EventUpdateView(generics.UpdateAPIView):
    """
    Organizers can update their own events.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        event = self.get_object()
        if event.organizer != self.request.user:
            raise PermissionError("You can only update your own events.")
        serializer.save()


class EventDeleteView(generics.DestroyAPIView):
    """
    Organizers can delete their own events.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.organizer != self.request.user:
            raise PermissionError("You can only delete your own events.")
        instance.delete()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]