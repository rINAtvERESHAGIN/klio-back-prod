from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import UserDetailSerializer, UserListSerializer

User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserDetailSerializer


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
