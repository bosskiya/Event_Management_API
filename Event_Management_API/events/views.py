from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from registrations.models import Registration
from .models import Event
from .serializers import EventSerializer, RegistrationSerializer
from .permissions import IsOrganizer, IsOwnerOrReadOnly

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOrganizer()]
        elif self.action == 'register':
            return [IsOwnerOrReadOnly()]
        return []

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        event = self.get_object()
        user = request.user

        # Check if event is full
        total_registrations = Registration.objects.filter(event=event, is_waitlisted=False).count()
        is_waitlisted = total_registrations >= event.capacity

        registration, created = Registration.objects.get_or_create(
            user=user, event=event,
            defaults={'is_waitlisted': is_waitlisted}
        )
        if not created:
            return Response({"detail": "Already registered."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Registered.", "waitlisted": is_waitlisted}, status=status.HTTP_201_CREATED)