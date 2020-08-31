import json
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .serializers import UserDetailSerializer

User = get_user_model()


class CurrentUserDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, context={'request': self.request})
        return Response(serializer.data)


class CurrentUserUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def update(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        if 'username' not in data or not data['username']:
            return Response({'username': ValidationError(_('Username can not be empty.'))},
                            status=HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=request.user.id, is_active=True)
        serializer = self.serializer_class(user, data=data, partial=True, context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
