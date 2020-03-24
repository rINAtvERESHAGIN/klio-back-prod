from rest_framework import generics

from .serializers import ContactDetailSerializer, ContactListSerializer, SocialListSerializer
from .models import Contact, SocialNet


class ContactCreateView(generics.CreateAPIView):
    serializer_class = ContactDetailSerializer


class ContactListView(generics.ListAPIView):
    serializer_class = ContactListSerializer
    queryset = Contact.objects.filter(activity=True)


class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContactDetailSerializer
    queryset = Contact.objects.all()


class SocialListView(generics.ListAPIView):
    serializer_class = SocialListSerializer
    queryset = SocialNet.objects.filter(activity=True)
