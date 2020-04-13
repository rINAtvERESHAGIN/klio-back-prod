from django.urls import path

from .views import ContactDetailView, ContactListView, SocialListView


urlpatterns = [
    path('list', ContactListView.as_view()),
    path('<int:pk>/detail', ContactDetailView.as_view()),
    path('socials/list', SocialListView.as_view()),
]
