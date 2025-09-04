from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Registration
from .serializers import RegistrationSerializer


class MyRegistrationsView(generics.ListAPIView):
    """
    List all events the current user is registered for.
    """
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Registration.objects.filter(user=self.request.user).select_related("event", "ticket_type")


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