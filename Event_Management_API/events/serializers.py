from rest_framework import serializers
from .models import Event, Session, Speaker, TicketType, Category
from django.utils import timezone


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ("id", "title", "speaker", "start_time", "end_time")


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ("id", "name", "price", "quantity")


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(source="organizer.id")
    sessions = SessionSerializer(many=True, required=False)
    ticket_types = TicketTypeSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = ("id", "title", "description", "date_time", "location", "capacity", "created_at", "organizer", "visibility", "image", "category", "sessions", "ticket_types", )

    def validate_date_time(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Event date/time must be in the future.")
        return value

    def create(self, validated_data):
        sessions_data = validated_data.pop("sessions", [])
        ttypes_data = validated_data.pop("ticket_types", [])
        event = Event.objects.create(**validated_data)

        for s in sessions_data:
            Session.objects.create(event=event, **s)

        for t in ttypes_data:
            TicketType.objects.create(event=event, **t)

        return event

    def update(self, instance, validated_data):
        sessions_data = validated_data.pop("sessions", [])
        ttypes_data = validated_data.pop("ticket_types", [])

        # Update main event fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Clear and recreate sessions
        if sessions_data:
            instance.sessions.all().delete()
            for s in sessions_data:
                Session.objects.create(event=instance, **s)

        # Clear and recreate ticket types
        if ttypes_data:
            instance.ticket_types.all().delete()
            for t in ttypes_data:
                TicketType.objects.create(event=instance, **t)

        return instance