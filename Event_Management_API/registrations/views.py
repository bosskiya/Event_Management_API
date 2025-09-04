from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Registration
from .serializers import RegistrationSerializer
from django.shortcuts import get_object_or_404
from events.models import Event, TicketType
from ticket.models import Ticket
from ticket.serializers import TicketSerializer
from rest_framework.decorators import api_view, permission_classes


class MyRegistrationsView(generics.ListAPIView):
    """
    List all events the current user is registered for.
    """
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Registration.objects.filter(user=self.request.user).select_related("event", "ticket_type")


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def register_for_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    ticket_type_id = request.data.get("ticket_type")
    ticket = None
    if ticket_type_id:
        ticket = get_object_or_404(TicketType, pk=ticket_type_id)

    try:
        reg = Registration.register(user=request.user, event=event, ticket_type=ticket)
    except ValueError as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(RegistrationSerializer(reg).data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def check_in_ticket(request, code):
    ticket = get_object_or_404(Ticket, code=code)
    # Only organizer of the event can check in
    if request.user != ticket.registration.event.organizer:
        return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

    ticket.mark_checked_in()
    return Response(TicketSerializer(ticket).data)


class RegisterForEventView(APIView):
    """
    Register the current user for an event.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            registration = serializer.save()
            return Response(
                RegistrationSerializer(registration).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)