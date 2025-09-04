from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, MeSerializer

User = get_user_model()

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = MeSerializer
    def get_object(self):
        return self.request.user