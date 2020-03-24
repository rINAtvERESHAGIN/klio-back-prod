from django.urls import path

from .views import ContactCreateView, ContactDetailView, ContactListView, SocialListView


urlpatterns = [
    path('create', ContactCreateView.as_view()),
    path('list', ContactListView.as_view()),
    path('<int:pk>/detail', ContactDetailView.as_view()),
    path('socials/list', SocialListView.as_view()),
]
