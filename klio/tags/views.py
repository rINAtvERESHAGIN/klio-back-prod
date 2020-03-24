from rest_framework import generics

from .serializers import TagDetailSerializer, TagListSerializer
from .models import Tag


class TagCreateView(generics.CreateAPIView):
    serializer_class = TagDetailSerializer


class TagListView(generics.ListAPIView):
    serializer_class = TagListSerializer
    queryset = Tag.objects.all()


class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagDetailSerializer
    queryset = Tag.objects.all()
