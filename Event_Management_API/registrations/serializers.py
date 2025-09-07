from rest_framework import serializers
from .models import Registration
from ticket.models import Ticket
from ticket.serializers import TicketSerializer
from events.models import Event, TicketType


class RegistrationSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(read_only=True)
    user = serializers.ReadOnlyField(source="user.id")
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    ticket_type = serializers.PrimaryKeyRelatedField(
        queryset=TicketType.objects.all(), required=False, allow_null=True
    )
    event_title = serializers.ReadOnlyField(source="event.title")

    class Meta:
        model = Registration
        fields = ("id", "user", "event", "ticket_type", "registered_at", "is_waitlisted", "ticket")
        read_only_fields = ("id", "user", "event", "registered_at", "is_waitlisted", "ticket")

    def validate(self, data):
        user = self.context["request"].user
        event = data["event"]

        # Prevent duplicate registration
        if Registration.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError("You are already registered for this event.")

        # Ensure ticket type belongs to this event
        ticket_type = data.get("ticket_type")
        if ticket_type and ticket_type.event != event:
            raise serializers.ValidationError("This ticket type does not belong to the selected event.")

        return data

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)