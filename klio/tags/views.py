from rest_framework import generics

from .serializers import TagSerializer
from .models import Tag


class TagCreateView(generics.CreateAPIView):
    serializer_class = TagSerializer


class TagListView(generics.ListAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.filter(activity=True)


class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
